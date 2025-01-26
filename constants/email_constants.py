import settings

FORGOT_PASSWORD_SUBJECT = "Reset your Pump password"
NO_REPLY_EMAIL = settings.NO_REPLY_EMAIL


def FORGOT_PASSWORD_BODY_TEXT(reset_password_url):
    return """Hello,

    We received a request to reset the password for your account associated with this email address.

    If you did not request a password reset, please ignore this email.

    To reset your password, please click the link below:

    {}

    This link will expire in 15 minutes.

    Thank you,
    The Pump Team""".format(
        reset_password_url
    )


def FORGOT_PASSWORD_BODY_HTML(reset_password_url):
    return f"""
    <html>
    <head></head>
    <body>
      <h2>Reset Your Password</h2>
      <p>Hello,</p>
      <p>We received a request to reset your password. Please click the link below to reset it:</p>
      <p><a href="{reset_password_url}" style="color: #5cb85c;">Reset Your Password</a></p>
      <p>If you didn't request this, please ignore this email.</p>
      <br>
      <p>Thanks, <br>The Pump Team</p>
    </body>
    </html>
    """
