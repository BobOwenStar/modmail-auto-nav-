from .nav import Nav

async def setup(bot):
    await bot.add_cog(Nav(bot))
