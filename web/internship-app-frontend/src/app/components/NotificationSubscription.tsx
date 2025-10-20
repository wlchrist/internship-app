'use client';

import React, { useState } from 'react';

interface NotificationFormData {
  email: string;
  phone: string;
  sms_enabled: boolean;
  daily_digest: boolean;
  instant_alerts: boolean;
  twilio_account_sid: string;
  twilio_auth_token: string;
  twilio_phone_number: string;
}

const NotificationSubscription: React.FC = () => {
  const [formData, setFormData] = useState<NotificationFormData>({
    email: '',
    phone: '',
    sms_enabled: true,
    daily_digest: true,
    instant_alerts: false,
    twilio_account_sid: '',
    twilio_auth_token: '',
    twilio_phone_number: '',
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState<'success' | 'error' | ''>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setMessage('');

    try {
      const response = await fetch('http://localhost:8000/notifications/subscribe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const result = await response.json();

      if (response.ok) {
        setMessage(`✅ Successfully subscribed! You'll receive SMS notifications at ${formData.phone}`);
        setMessageType('success');
        setFormData({
          email: '',
          phone: '',
          sms_enabled: true,
          daily_digest: true,
          instant_alerts: false,
          twilio_account_sid: '',
          twilio_auth_token: '',
          twilio_phone_number: '',
        });
      } else {
        setMessage(`❌ Error: ${result.detail}`);
        setMessageType('error');
      }
    } catch (error) {
      setMessage('❌ Network error. Please try again.');
      setMessageType('error');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleUnsubscribe = async () => {
    if (!formData.email) {
      setMessage('❌ Please enter your email address to unsubscribe');
      setMessageType('error');
      return;
    }

    setIsSubmitting(true);
    setMessage('');

    try {
      const response = await fetch('http://localhost:8000/notifications/unsubscribe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData.email),
      });

      const result = await response.json();

      if (response.ok) {
        setMessage('✅ Successfully unsubscribed from notifications');
        setMessageType('success');
        setFormData({
          email: '',
          phone: '',
          sms_enabled: true,
          daily_digest: true,
          instant_alerts: false,
          twilio_account_sid: '',
          twilio_auth_token: '',
          twilio_phone_number: '',
        });
      } else {
        setMessage(`❌ Error: ${result.detail}`);
        setMessageType('error');
      }
    } catch (error) {
      setMessage('❌ Network error. Please try again.');
      setMessageType('error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">
          📱 Get SMS Notifications for New Internships
        </h2>
        <p className="text-gray-600">
          Stay updated with the latest CS internship opportunities via SMS
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Email Field (for identification) */}
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
            Email Address (for account identification) *
          </label>
          <input
            type="email"
            id="email"
            required
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="your.email@example.com"
          />
        </div>

        {/* Phone Number Field */}
        <div>
          <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-2">
            Phone Number *
          </label>
          <input
            type="tel"
            id="phone"
            required
            value={formData.phone}
            onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="1234567890"
          />
        </div>

        {/* Twilio Credentials Section */}
        <div className="space-y-4">
          <h3 className="text-lg font-medium text-gray-900">Twilio SMS Credentials (Optional)</h3>
          <p className="text-sm text-gray-600">
            Provide your own Twilio credentials to use your account, or leave blank to use system defaults.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="twilio_account_sid" className="block text-sm font-medium text-gray-700 mb-2">
                Twilio Account SID
              </label>
              <input
                type="text"
                id="twilio_account_sid"
                value={formData.twilio_account_sid}
                onChange={(e) => setFormData({ ...formData, twilio_account_sid: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
              />
            </div>
            
            <div>
              <label htmlFor="twilio_auth_token" className="block text-sm font-medium text-gray-700 mb-2">
                Twilio Auth Token
              </label>
              <input
                type="password"
                id="twilio_auth_token"
                value={formData.twilio_auth_token}
                onChange={(e) => setFormData({ ...formData, twilio_auth_token: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Your auth token"
              />
            </div>
          </div>
          
          <div>
            <label htmlFor="twilio_phone_number" className="block text-sm font-medium text-gray-700 mb-2">
              Twilio Phone Number
            </label>
            <input
              type="tel"
              id="twilio_phone_number"
              value={formData.twilio_phone_number}
              onChange={(e) => setFormData({ ...formData, twilio_phone_number: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="+1234567890"
            />
          </div>
        </div>

        {/* Notification Preferences */}
        <div className="space-y-4">
          <h3 className="text-lg font-medium text-gray-900">Notification Preferences</h3>
          <div className="flex items-center space-x-3">
            <input
              type="checkbox"
              id="daily_digest"
              checked={formData.daily_digest}
              onChange={(e) => setFormData({ ...formData, daily_digest: e.target.checked })}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="daily_digest" className="text-sm font-medium text-gray-700">
              📅 Daily SMS digest with new internships
            </label>
          </div>

          <div className="flex items-center space-x-3">
            <input
              type="checkbox"
              id="instant_alerts"
              checked={formData.instant_alerts}
              onChange={(e) => setFormData({ ...formData, instant_alerts: e.target.checked })}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="instant_alerts" className="text-sm font-medium text-gray-700">
              ⚡ Instant SMS alerts for urgent opportunities
            </label>
          </div>
        </div>

        {/* Message Display */}
        {message && (
          <div className={`p-4 rounded-lg ${
            messageType === 'success' 
              ? 'bg-green-50 text-green-800 border border-green-200' 
              : 'bg-red-50 text-red-800 border border-red-200'
          }`}>
            {message}
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex space-x-4">
          <button
            type="submit"
            disabled={isSubmitting}
            className="flex-1 bg-blue-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-blue-700 disabled:bg-blue-400 disabled:cursor-not-allowed transition-colors"
          >
            {isSubmitting ? 'Subscribing...' : 'Subscribe to SMS Notifications'}
          </button>
          
          <button
            type="button"
            onClick={handleUnsubscribe}
            disabled={isSubmitting || !formData.email}
            className="flex-1 bg-gray-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-gray-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            Unsubscribe
          </button>
        </div>
      </form>

      {/* Info Section */}
      <div className="mt-8 p-4 bg-blue-50 rounded-lg">
        <h4 className="font-medium text-blue-900 mb-2">ℹ️ How SMS notifications work:</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• <strong>Your Twilio Account:</strong> Use your own Twilio credentials (recommended)</li>
          <li>• <strong>System Defaults:</strong> Leave credentials blank to use system defaults</li>
          <li>• <strong>Free Tier:</strong> Twilio offers $15 free credit (enough for ~2,000 SMS)</li>
          <li>• <strong>Daily digest:</strong> Summary of new internships every 24 hours</li>
          <li>• <strong>Instant alerts:</strong> Immediate SMS for urgent opportunities</li>
          <li>• <strong>Easy unsubscribe:</strong> Reply STOP to any SMS</li>
        </ul>
        
        <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded">
          <p className="text-sm text-yellow-800">
            <strong>🔒 Security:</strong> Your Twilio credentials are stored securely and only used for your SMS notifications.
          </p>
        </div>
      </div>
    </div>
  );
};

export default NotificationSubscription;