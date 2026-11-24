"""Synthetic demo messages only.

Every message below was invented for this portfolio project. There are no
real phishing emails, no real inboxes, and no live data in this repo.
Labels: 1 = phishing-like, 0 = legitimate.
"""

SYNTHETIC_MESSAGES = [
    # Phishing-like (label 1)
    (1, "Urgent: your account will be suspended in 24 hours, verify now by clicking the link below"),
    (1, "Congratulations, you have won a prize, claim your reward by entering your password"),
    (1, "Your payment failed, update your billing details immediately to avoid account closure"),
    (1, "Security alert: unusual login detected, confirm your identity now or lose access"),
    (1, "Your package could not be delivered, click here to reschedule and pay the fee"),
    (1, "Dear customer, your bank account needs verification, login here before midnight"),
    (1, "You have received a refund, click the link to claim it before it expires"),
    (1, "Action required: your password expires today, reset it using this link"),
    (1, "Your invoice is overdue, download the attachment to view your payment details"),
    (1, "We detected suspicious activity, verify your account now to avoid suspension"),
    (1, "Free gift waiting for you, enter your card details to claim your prize"),
    (1, "Your subscription will be cancelled, confirm your payment method immediately"),
    # Legitimate (label 0)
    (0, "Hi team, here are the notes from today's meeting and the action items for next week"),
    (0, "Your order has shipped, tracking number is included and delivery is expected on Friday"),
    (0, "Reminder: our weekly team call is on Thursday at 10am, agenda attached"),
    (0, "Thank you for your purchase, your receipt is attached to this email"),
    (0, "Hi, I have updated the project document with the latest figures, please review when you can"),
    (0, "Your appointment is confirmed for Monday at 3pm, reply if you need to reschedule"),
    (0, "The quarterly report is ready, the summary is in the first section"),
    (0, "Welcome to our newsletter, here is this month's update from the team"),
    (0, "Hi, can we move our call to tomorrow afternoon, the morning is busy"),
    (0, "Your password was changed successfully, if this was not you please contact support"),
    (0, "The training session slides are attached, let me know if you have questions"),
    (0, "Invoice for your monthly plan is attached, no action needed, it will be charged as usual"),
]
