import requests
from app.core.config import settings
import os
from dotenv import load_dotenv

load_dotenv()
email_url = os.getenv("SENDGRID_URL")

def send_otp_email(email: str, otp: str, username: str):
    """Send an OTP email using SendGrid."""
    url = email_url
    headers = {
        "Authorization": f"Bearer {settings.SENDGRID_API_KEY}",
        "Content-Type": "application/json",
    }

    frontend_domain = settings.FRONTEND_DOMAIN

    payload = {
        "personalizations": [{
            "to": [{"email": email}],
            "subject": "Your OTP Code - Gregor Jeffrey Cognitive Preference Indicator",
        }],
        "from": {"email": "warismstf@gmail.com", "name": "Gregor Jeffrey Support"},
        "content": [{
            "type": "text/html",
            "value": f"""
                <html>
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>OTP Verification</title>
                        <style>
                            body {{
                                font-family: 'Arial', sans-serif;
                                background-color: #fff;
                                color: #000;
                                margin: 0;
                                padding: 0;
                                text-align: center;
                            }}
                            .email-container {{
                                max-width: 600px;
                                margin: 0 auto;
                                background: #fff;
                                padding: 30px;
                                border-radius: 10px;
                                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                            }}
                            .header {{
                                background: #000;
                                padding: 20px;
                                border-radius: 10px 10px 0 0;
                                color: #fff;
                                text-align: center;
                            }}
                            .header h1 {{
                                font-size: 36px;
                                margin: 0;
                                font-weight: bold;
                            }}
                            .header h2 {{
                                font-size: 18px;
                                margin: 5px 0 0;
                            }}
                            .content p {{
                                font-size: 16px;
                                line-height: 1.5;
                                margin: 10px 0;
                            }}
                            .otp {{
                                font-size: 24px;
                                font-weight: bold;
                                color: #000;
                                background: #eee;
                                padding: 10px 20px;
                                display: inline-block;
                                border-radius: 5px;
                                margin-top: 15px;
                            }}
                            .footer {{
                                margin-top: 20px;
                                font-size: 12px;
                                color: #aaa;
                            }}
                            .footer a {{
                                color: #000;
                                text-decoration: none;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="email-container">
                            <div class="header">
                                <h1>Gregor Jeffrey</h1>
                                <h2>Cognitive Preference Indicator</h2>
                            </div>
                            <div class="content">
                                <p>Dear {username},</p>
                                <p>Thank you for requesting an OTP. Please use the following One-Time Password (OTP) to verify your email address:</p>
                                <p class="otp">{otp}</p>
                                <p>If you did not request this OTP, please ignore this email.</p>
                            </div>
                            <div class="footer">
                                <p>Best regards,<br>Gregor Jeffrey Support Team</p>
                                <p><a href="{frontend_domain}/help">Need Help?</a></p>
                            </div>
                        </div>
                    </body>
                </html>
            """
        }]
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

def send_reset_link_email(email: str, reset_link: str, username: str):
    """Send password reset email using SendGrid."""
    url = email_url
    headers = {
        "Authorization": f"Bearer {settings.SENDGRID_API_KEY}",
        "Content-Type": "application/json",
    }

    frontend_domain = settings.FRONTEND_DOMAIN

    payload = {
        "personalizations": [{
            "to": [{"email": email}],
            "subject": "Reset Your Password - Gregor Jeffrey Cognitive Preference Indicator",
        }],
        "from": {"email": "warismstf@gmail.com", "name": "Gregor Jeffrey Support"},
        "content": [{
            "type": "text/html",
            "value": f"""
                <html>
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Reset Password</title>
                        <style>
                            body {{
                                font-family: 'Arial', sans-serif;
                                background-color: #fff;
                                color: #000;
                                margin: 0;
                                padding: 0;
                                text-align: center;
                            }}
                            .email-container {{
                                max-width: 600px;
                                margin: 0 auto;
                                background: #fff;
                                padding: 30px;
                                border-radius: 10px;
                                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                            }}
                            .header {{
                                background: #000;
                                padding: 20px;
                                border-radius: 10px 10px 0 0;
                                color: #fff;
                                text-align: center;
                            }}
                            .header h1 {{
                                font-size: 36px;
                                margin: 0;
                                font-weight: bold;
                            }}
                            .header h2 {{
                                font-size: 18px;
                                margin: 5px 0 0;
                            }}
                            .content p {{
                                font-size: 16px;
                                line-height: 1.5;
                                margin: 10px 0;
                            }}
                            .button {{
                                display: inline-block;
                                padding: 12px 25px;
                                background: #000;
                                color: #fff;
                                text-decoration: none;
                                border-radius: 5px;
                                font-size: 16px;
                                margin-top: 20px;
                            }}
                            .footer {{
                                margin-top: 20px;
                                font-size: 12px;
                                color: #aaa;
                            }}
                            .footer a {{
                                color: #000;
                                text-decoration: none;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="email-container">
                            <div class="header">
                                <h1>Gregor Jeffrey</h1>
                                <h2>Cognitive Preference Indicator</h2>
                            </div>
                            <div class="content">
                                <p>Dear {username},</p>
                                <p>To reset your password, click the button below:</p>
                                <p><a href="{reset_link}" class="button">Reset Password</a></p>
                                <p>If you did not request this, please ignore this email.</p>
                            </div>
                            <div class="footer">
                                <p>Best regards,<br>Gregor Jeffrey Support Team</p>
                                <p><a href="{frontend_domain}/help">Need Help?</a></p>
                            </div>
                        </div>
                    </body>
                </html>
            """
        }]
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
