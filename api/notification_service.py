import os
from typing import List, Optional
from datetime import datetime
import logging
from models import Internship, NotificationPreferences, Carrier

# Twilio SMS integration (no email required)
try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False
    print("Twilio not available. Install with: pip install twilio")

# Fallback to email gateways if Twilio not available
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class NotificationService:
    """Service for sending email and SMS notifications"""
    
    def __init__(self):
        # Twilio SMS configuration (no personal email required)
        self.twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
        
        # Initialize Twilio if available
        if TWILIO_AVAILABLE and self.twilio_account_sid and self.twilio_auth_token:
            self.twilio_client = Client(self.twilio_account_sid, self.twilio_auth_token)
            self.use_twilio = True
            logging.info("Using Twilio for SMS notifications")
        else:
            self.twilio_client = None
            self.use_twilio = False
            logging.info("Using email gateway fallback for SMS notifications")
        
        # Fallback email gateway configuration
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email_user = os.getenv("NOTIFICATION_EMAIL", "your-app@gmail.com")
        self.email_password = os.getenv("NOTIFICATION_PASSWORD", "your-app-password")
        
        # SMS via email gateways (completely free)
        self.carrier_gateways = {
            Carrier.VERIZON: "vtext.com",
            Carrier.ATT: "txt.att.net",
            Carrier.TMOBILE: "tmomail.net",
            Carrier.SPRINT: "messaging.sprintpcs.com",
            Carrier.US_CELLULAR: "email.uscc.net"
        }
        
        # In-memory storage for demo (replace with database in production)
        self.subscribers: List[NotificationPreferences] = []
        
    async def subscribe_user(self, preferences: NotificationPreferences) -> bool:
        """Subscribe a user to notifications"""
        try:
            # Check if user already exists
            existing_user = next(
                (user for user in self.subscribers if user.email == preferences.email), 
                None
            )
            
            if existing_user:
                # Update existing user
                index = self.subscribers.index(existing_user)
                self.subscribers[index] = preferences
                logging.info(f"Updated notification preferences for {preferences.email}")
            else:
                # Add new user
                self.subscribers.append(preferences)
                logging.info(f"Subscribed {preferences.email} to notifications")
            
            return True
        except Exception as e:
            logging.error(f"Error subscribing user: {e}")
            return False
    
    async def unsubscribe_user(self, email: str) -> bool:
        """Unsubscribe a user from notifications"""
        try:
            self.subscribers = [user for user in self.subscribers if user.email != email]
            logging.info(f"Unsubscribed {email} from notifications")
            return True
        except Exception as e:
            logging.error(f"Error unsubscribing user: {e}")
            return False
    
    async def send_daily_digest(self, internships: List[Internship]) -> int:
        """Send daily digest to all subscribers"""
        if not internships:
            return 0
            
        sent_count = 0
        
        for subscriber in self.subscribers:
            if not subscriber.daily_digest:
                continue
                
            try:
                # Send email
                await self._send_email(
                    subscriber.email,
                    "Daily CS Internship Digest",
                    self._create_digest_html(internships)
                )
                
                # Send SMS if enabled
                if subscriber.sms_enabled and subscriber.phone:
                    sms_message = self._create_digest_sms(internships)
                    await self._send_sms(subscriber.phone, sms_message, subscriber)
                
                sent_count += 1
                logging.info(f"Sent daily digest to {subscriber.email}")
                
            except Exception as e:
                logging.error(f"Error sending digest to {subscriber.email}: {e}")
        
        return sent_count
    
    async def send_instant_alert(self, new_internships: List[Internship]) -> int:
        """Send instant alerts for new internships"""
        if not new_internships:
            return 0
            
        sent_count = 0
        
        for subscriber in self.subscribers:
            if not subscriber.instant_alerts:
                continue
                
            try:
                # Send email
                await self._send_email(
                    subscriber.email,
                    "New CS Internships Available!",
                    self._create_alert_html(new_internships)
                )
                
                # Send SMS if enabled
                if subscriber.sms_enabled and subscriber.phone:
                    sms_message = self._create_alert_sms(new_internships)
                    await self._send_sms(subscriber.phone, sms_message, subscriber)
                
                sent_count += 1
                logging.info(f"Sent instant alert to {subscriber.email}")
                
            except Exception as e:
                logging.error(f"Error sending alert to {subscriber.email}: {e}")
        
        return sent_count
    
    async def _send_email(self, to_email: str, subject: str, html_content: str) -> bool:
        """Send email using SendGrid or SMTP fallback"""
        if self.use_sendgrid:
            return await self._send_email_sendgrid(to_email, subject, html_content)
        else:
            return await self._send_email_smtp(to_email, subject, html_content)
    
    async def _send_email_sendgrid(self, to_email: str, subject: str, html_content: str) -> bool:
        """Send email using SendGrid API"""
        try:
            message = Mail(
                from_email=self.from_email,
                to_emails=to_email,
                subject=subject,
                html_content=html_content
            )
            
            response = self.sg.send(message)
            if response.status_code in [200, 201, 202]:
                logging.info(f"Email sent successfully to {to_email} via SendGrid")
                return True
            else:
                logging.error(f"SendGrid error: {response.status_code}")
                return False
                
        except Exception as e:
            logging.error(f"Error sending email via SendGrid to {to_email}: {e}")
            return False
    
    async def _send_email_smtp(self, to_email: str, subject: str, html_content: str) -> bool:
        """Send email using SMTP (fallback)"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.email_user
            msg['To'] = to_email
            
            # Create HTML part
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.send_message(msg)
            
            logging.info(f"Email sent successfully to {to_email} via SMTP")
            return True
        except Exception as e:
            logging.error(f"Error sending email via SMTP to {to_email}: {e}")
            return False
    
    async def _send_sms(self, phone_number: str, message: str, subscriber: NotificationPreferences = None) -> bool:
        """Send SMS using Twilio or email gateway fallback"""
        if self.use_twilio or (subscriber and subscriber.twilio_account_sid):
            return await self._send_sms_twilio(phone_number, message, subscriber)
        else:
            return await self._send_sms_via_email(phone_number, message)
    
    async def _send_sms_twilio(self, phone_number: str, message: str, subscriber: NotificationPreferences = None) -> bool:
        """Send SMS using Twilio API (user credentials or system defaults)"""
        try:
            # Use user's credentials if provided, otherwise use system defaults
            if subscriber and subscriber.twilio_account_sid and subscriber.twilio_auth_token:
                client = Client(subscriber.twilio_account_sid, subscriber.twilio_auth_token)
                from_number = subscriber.twilio_phone_number or self.twilio_phone_number
                logging.info(f"Using user's Twilio credentials for {subscriber.email}")
            else:
                client = self.twilio_client
                from_number = self.twilio_phone_number
                logging.info("Using system Twilio credentials")
            
            # Clean phone number (remove non-digits)
            clean_phone = ''.join(filter(str.isdigit, phone_number))
            
            # Add country code if not present
            if not clean_phone.startswith('1') and len(clean_phone) == 10:
                clean_phone = f"+1{clean_phone}"
            elif not clean_phone.startswith('+'):
                clean_phone = f"+{clean_phone}"
            
            # Send SMS via Twilio
            message_obj = client.messages.create(
                body=message,
                from_=from_number,
                to=clean_phone
            )
            
            logging.info(f"SMS sent successfully to {clean_phone} via Twilio (SID: {message_obj.sid})")
            return True
            
        except Exception as e:
            logging.error(f"Error sending SMS via Twilio to {phone_number}: {e}")
            return False
    
    async def _send_sms_via_email(self, phone_number: str, message: str) -> bool:
        """Send SMS via email gateway (fallback)"""
        try:
            # Clean phone number (remove non-digits)
            clean_phone = ''.join(filter(str.isdigit, phone_number))
            
            # Try all carriers (since we don't know which one)
            for carrier, gateway in self.carrier_gateways.items():
                try:
                    sms_email = f"{clean_phone}@{gateway}"
                    
                    # Send email to SMS gateway
                    await self._send_email_smtp(
                        sms_email,
                        "",  # No subject for SMS
                        message
                    )
                    
                    logging.info(f"SMS sent to {clean_phone} via {carrier} gateway")
                    return True
                    
                except Exception as e:
                    logging.debug(f"Failed to send via {carrier}: {e}")
                    continue
            
            logging.error(f"Failed to send SMS to {phone_number} via all carriers")
            return False
            
        except Exception as e:
            logging.error(f"Error sending SMS to {phone_number}: {e}")
            return False
    
    def _create_digest_html(self, internships: List[Internship]) -> str:
        """Create HTML content for daily digest"""
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #2563eb; color: white; padding: 20px; border-radius: 8px; }}
                .internship {{ border: 1px solid #e5e7eb; margin: 15px 0; padding: 15px; border-radius: 8px; }}
                .title {{ font-size: 18px; font-weight: bold; color: #1f2937; }}
                .company {{ color: #6b7280; font-size: 14px; }}
                .location {{ color: #6b7280; font-size: 14px; }}
                .description {{ margin: 10px 0; color: #374151; }}
                .salary {{ color: #059669; font-weight: bold; }}
                .link {{ color: #2563eb; text-decoration: none; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎯 Daily CS Internship Digest</h1>
                <p>Found {len(internships)} new Computer Science internships for you!</p>
            </div>
        """
        
        for internship in internships[:10]:  # Limit to top 10
            html += f"""
            <div class="internship">
                <div class="title">{internship.title}</div>
                <div class="company">🏢 {internship.company}</div>
                <div class="location">📍 {internship.location}</div>
                <div class="description">{internship.description[:200]}...</div>
                {f'<div class="salary">💰 {internship.salary}</div>' if internship.salary else ''}
                <a href="{internship.source_url}" class="link">View Job →</a>
            </div>
            """
        
        html += """
            <div style="margin-top: 30px; padding: 20px; background-color: #f9fafb; border-radius: 8px;">
                <p>💡 <strong>Tip:</strong> Visit our website to see all internships and set up instant alerts!</p>
                <p>📧 <strong>Unsubscribe:</strong> Reply to this email with "UNSUBSCRIBE"</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _create_digest_sms(self, internships: List[Internship]) -> str:
        """Create SMS content for daily digest"""
        message = f"🎯 CS Internship Digest: {len(internships)} new opportunities!\n\n"
        
        for i, internship in enumerate(internships[:3], 1):  # Limit to top 3 for SMS
            message += f"{i}. {internship.title} @ {internship.company}\n"
            message += f"   📍 {internship.location}\n"
            if internship.salary:
                message += f"   💰 {internship.salary}\n"
            message += "\n"
        
        if len(internships) > 3:
            message += f"...and {len(internships) - 3} more! Visit our website for details."
        
        return message
    
    def _create_alert_html(self, internships: List[Internship]) -> str:
        """Create HTML content for instant alerts"""
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #dc2626; color: white; padding: 20px; border-radius: 8px; }}
                .internship {{ border: 1px solid #e5e7eb; margin: 15px 0; padding: 15px; border-radius: 8px; }}
                .title {{ font-size: 18px; font-weight: bold; color: #1f2937; }}
                .company {{ color: #6b7280; font-size: 14px; }}
                .location {{ color: #6b7280; font-size: 14px; }}
                .description {{ margin: 10px 0; color: #374151; }}
                .salary {{ color: #059669; font-weight: bold; }}
                .link {{ color: #2563eb; text-decoration: none; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚨 New CS Internships Available!</h1>
                <p>{len(internships)} fresh opportunities just posted!</p>
            </div>
        """
        
        for internship in internships:
            html += f"""
            <div class="internship">
                <div class="title">{internship.title}</div>
                <div class="company">🏢 {internship.company}</div>
                <div class="location">📍 {internship.location}</div>
                <div class="description">{internship.description[:200]}...</div>
                {f'<div class="salary">💰 {internship.salary}</div>' if internship.salary else ''}
                <a href="{internship.source_url}" class="link">Apply Now →</a>
            </div>
            """
        
        html += """
            <div style="margin-top: 30px; padding: 20px; background-color: #f9fafb; border-radius: 8px;">
                <p>⚡ <strong>Act Fast:</strong> These internships are fresh and competition is high!</p>
                <p>📧 <strong>Unsubscribe:</strong> Reply to this email with "UNSUBSCRIBE"</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _create_alert_sms(self, internships: List[Internship]) -> str:
        """Create SMS content for instant alerts"""
        message = f"🚨 NEW CS INTERNSHIPS! {len(internships)} just posted:\n\n"
        
        for i, internship in enumerate(internships[:2], 1):  # Limit to top 2 for SMS
            message += f"{i}. {internship.title} @ {internship.company}\n"
            message += f"   📍 {internship.location}\n\n"
        
        if len(internships) > 2:
            message += f"...and {len(internships) - 2} more! Apply fast!"
        
        return message
    
    def get_subscriber_count(self) -> int:
        """Get total number of subscribers"""
        return len(self.subscribers)
    
    def get_subscribers(self) -> List[NotificationPreferences]:
        """Get all subscribers (for admin purposes)"""
        return self.subscribers.copy()
