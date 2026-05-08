from .nav import SupportDepartments

async def setup(bot):
    await bot.add_cog(SupportDepartments(bot))
