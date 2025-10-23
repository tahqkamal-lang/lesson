import discord
from discord.ext import commands
from math import ceil

# إعداد البوت
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# الأسعار
prices = {
    "semi": 3000,
    "teacher": 6000,
    "master": 10000
}

ADMIN_PERCENT = 0.20   # نسبة الإدارة
PROBOT_PERCENT = 0.05  # نسبة خصم البرو بوت (5%)

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')

@bot.command()
async def price(ctx, category: str, sessions: int):
    category = category.lower()

    if category not in prices:
        await ctx.send("❌ الفئة غير صحيحة! استخدم: semi, teacher, master")
        return

    # الحسابات الأساسية
    base_price = prices[category] * sessions
    admin_share = base_price * ADMIN_PERCENT
    teacher_share = base_price - admin_share

    # حساب مبلغ الإرسال الصحيح بعد خصم 5%
    must_send_teacher = ceil(teacher_share / (1 - PROBOT_PERCENT))
    probot_fee_teacher = must_send_teacher - teacher_share

    must_send_admin = ceil(admin_share / (1 - PROBOT_PERCENT))
    probot_fee_admin = must_send_admin - admin_share

    embed = discord.Embed(title="💰 تفاصيل الحصص", color=0x2ecc71)
    embed.add_field(name="📚 الفئة", value=category.capitalize(), inline=True)
    embed.add_field(name="📆 عدد الحصص", value=sessions, inline=True)
    embed.add_field(name="💵 السعر الكلي", value=f"{base_price:,.0f}", inline=False)
    embed.add_field(name="🏢 نسبة الإدارة (20%)", value=f"{admin_share:,.0f}", inline=False)
    embed.add_field(name="👨‍🏫 نصيب المدرس", value=f"{teacher_share:,.0f}", inline=False)

    embed.add_field(
        name="💸 تحويل الإدارة عبر ProBot",
        value=(
            f"🔹 أرسل **{must_send_admin:,}** ليستلم الحساب الإداري **{admin_share:,.0f}** بعد خصم **{probot_fee_admin:,.0f}**."
        ),
        inline=False
    )

    embed.add_field(
        name="💸 تحويل المدرس عبر ProBot",
        value=(
            f"🔹 أرسل **{must_send_teacher:,}** ليستلم المدرس **{teacher_share:,.0f}** بعد خصم **{probot_fee_teacher:,.0f}**."
        ),
        inline=False
    )

    await ctx.send(embed=embed)

bot.run("MTQzMDg5NTMwMzYyNzg5ODg4MA.GFFY8G.-0rtpH8BGx0wBwnD6mamdTAX9X5OiDT8v8KM5s")
