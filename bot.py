import pubchempy as pcp
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, filters

# Replace 'YOUR_BOT_TOKEN' with the actual token for your Telegram bot
TOKEN = 'YOUR_BOT_TOKEN'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to the Chemical Info Bot! Send me a chemical formula to get information.')

def chemical_info(update: Update, context: CallbackContext) -> None:
    chemical_formula = update.message.text

    try:
        # Search PubChem for the compound by its chemical formula
        compound = pcp.get_compounds(chemical_formula, 'formula')[0]

        # Display information about the compound
        info_message = (
            f"Name: {compound.iupac_name}\n"
            f"Common Name: {compound.synonyms[0]}\n"
            f"Molecular Weight: {compound.molecular_weight}\n"
            f"Formula: {compound.molecular_formula}"
        )

        # Send the information back to the user
        update.message.reply_text(info_message)

    except IndexError:
        update.message.reply_text(f"No information found for {chemical_formula}. Please check the formula.")

def main() -> None:
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(filters.Text & ~filters.Command, chemical_info))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
