# cryptoprice-discordbot

This discord bot follows the BTC/USD price using the Pyth Oracle (https://pyth.network/), but can be changed to any asset available on the Pyth Network. 

![Snímek obrazovky 2023-09-26 082247](https://github.com/0xmakerr/cryptoprice-discordbot/assets/25880864/d447674a-cb44-4183-a312-f33923253802)

To track a different asset, simply change the `SOLANA_PRICE_ID` in the `pyth.py` file to a different price feed ID (https://pyth.network/developers/price-feed-ids#solana-mainnet-beta) and `PYTH_EVM_PRICE_ID` (https://pyth.network/developers/price-feed-ids#pyth-evm-mainnet).

## Setup
The bot works out of the box after inviting it to your server *(may take up to a minute to start displaying prices)*, however, for color change based on 24h Change % to work, we have to follow some steps first:

1) [Invite the bot to your server](https://discord.com/api/oauth2/authorize?client_id=1150124229224824983&permissions=335546368&scope=bot)
2) Create a new discord role and assign it to the bot (in our example we named the new role "Pyth Price"). You need to enable [Manage Roles permission](https://github.com/0xmakerr/cryptoprice-discordbot/assets/25880864/b1f58c6a-eaa3-4d2e-bafb-3af81d06ec61) to this new role, so that the bot can change it's role color.
3) Move the new role hierarchicaly above the default role of the bot (which in our case means above the "BTC" role).

![Snímek obrazovky 2023-09-26 085639](https://github.com/0xmakerr/cryptoprice-discordbot/assets/25880864/561f27f6-4a27-41aa-ae63-7646d0c7fde2)
