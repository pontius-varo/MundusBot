
# Add your custom commands here | If you plan on writing one, I strongly recommend checking out the telegram API docs
def samsayingyes(update, context):
    custom_sticker = 'CAACAgEAAxkBAAEDMilhftTjxn88VqCiCqYhGh0XxD8T9AACIAIAAjzdyEe2g_Klt73eNCEE'
    context.bot.send_sticker(
            chat_id=update.effective_chat.id, sticker=custom_sticker)


# Always have this object at the last line | Add your custom commands to this dict
custom_cmds = {'samsayingyes': samsayingyes}
