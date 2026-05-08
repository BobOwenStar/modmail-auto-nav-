import discord
from discord.ext import commands

# -----------------------------
# NAVIGATION MESSAGE (ON OPEN)
# -----------------------------
NAV_MESSAGE = """# <:Logo:1476596990832939078> Support Navigation

Welcome to **Aspect Hosting**. To ensure your inquiry is handled by the appropriate specialist, please identify your department of concern from the options below.

If you havent already, please __**try the AI in https://discord.com/channels/1475555607212986441/1476484258993279026 before we can assist you any further**__

**01** ‣ My concern regards the **General Inquiry** department.
**02** ‣ My concern regards the **Technical Support** department.
**03** ‣ My concern regards the **Billing & Finance** department.
**04** ‣ My concern regards the **Emergency Response** department.
**05** ‣ My concern regards the **Public Relations** department.
**06** ‣ My concern regards the **Legal & Abuse** department.
"""


# -----------------------------
# DEPARTMENT MESSAGES
# -----------------------------
DEPARTMENTS = {
    "1": "general",
    "01": "general",
    "general": "general",

    "2": "technical",
    "02": "technical",
    "tech": "technical",
    "technical": "technical",

    "3": "billing",
    "03": "billing",
    "billing": "billing",
    "finance": "billing",

    "4": "emergency",
    "04": "emergency",
    "emergency": "emergency",

    "5": "pr",
    "05": "pr",
    "public relations": "pr",
    "pr": "pr",

    "6": "legal",
    "06": "legal",
    "legal": "legal",
    "abuse": "legal",
}


INTRO_MESSAGES = {
    "general": """<:Logo:1476596990832939078> General Inquiry

Welcome to **Aspect Hosting – General Inquiry**.

This department handles:
• General questions about our services
• Pre-sales enquiries
• Basic information requests

A member of our team will assist you shortly.

**Estimated Wait Time**: 10 Minutes""",

    "technical": """<:Logo:1476596990832939078> Technical Support

Welcome to **Aspect Hosting – Technical Support**.

This department handles:
• Server issues and errors
• Downtime or performance problems
• Setup and configuration help

Please provide as much detail as possible for faster support.

**Estimated Wait Time**: 10 Minutes""",

    "billing": """<:Logo:1476596990832939078> Billing & Finance

Welcome to **Aspect Hosting – Billing & Finance**.

This department handles:
• Payments and invoices
• Subscription issues
• Refund requests

Please include your invoice ID if applicable.

**Estimated Wait Time**: 5 Minutes""",

    "emergency": """<:Logo:1476596990832939078> Emergency Response

Welcome to **Aspect Hosting – Emergency Response**.

This department is for:
• Critical outages
• Security breaches
• Urgent service disruptions

Tickets here are prioritised immediately.

**Estimated Wait Time**: Immediate Response""",

    "pr": """<:Logo:1476596990832939078> Public Relations

Welcome to **Aspect Hosting – Public Relations**.

This department handles:
• Partnerships and collaborations
• Media enquiries
• Brand-related questions

Our PR team will respond as soon as possible.

**Estimated Wait Time**: 15 Minutes""",

    "legal": """<:Logo:1476596990832939078> Legal & Abuse

Welcome to **Aspect Hosting – Legal & Abuse.**

This department handles:
• Abuse reports
• Terms of Service violations
• Legal requests

Please provide clear evidence when submitting your report.

**Estimated Wait Time**: 15 Minutes"""
}


class SupportDepartments(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.opened_tickets = set()      # navigation sent
        self.activated_tickets = set()   # department chosen

    # -----------------------------
    # 1. SEND NAV ON TICKET OPEN
    # -----------------------------
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        channel = message.channel

        if not isinstance(channel, discord.TextChannel):
            return

        # only run in ticket channels (adjust if needed)
        if "ticket" not in channel.name.lower():
            return

        # -----------------------------
        # SEND NAVIGATION ONCE
        # -----------------------------
        if channel.id not in self.opened_tickets:
            self.opened_tickets.add(channel.id)
            await channel.send(NAV_MESSAGE)

        # -----------------------------
        # DEPARTMENT DETECTION
        # -----------------------------
        content = message.content.lower().strip()

        dept = DEPARTMENTS.get(content)
        if not dept:
            return

        # only allow once per ticket
        if channel.id in self.activated_tickets:
            return

        self.activated_tickets.add(channel.id)

        response = INTRO_MESSAGES.get(dept)
        if response:
            await channel.send(response)


# -----------------------------
# REGISTER COG
# -----------------------------
async def setup(bot):
    await bot.add_cog(SupportDepartments(bot))
