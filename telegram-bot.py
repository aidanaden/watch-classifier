from fastai.vision import *
from fastai.widgets import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import telegram

# FASTAI 
defaults.device = torch.device('cpu')
learner_pth = Path('C:\\Users\\Aidan\\Documents\\DL Practice\\data\\watch_brands\\models')
learner_name = '1024-resnet34-90-watch-classification.pkl'
learner = load_learner(learner_pth, learner_name)

updater = Updater(token='847588157:AAEZoJzdNwKzPsxaKGOKhDqV9XYqoQtZYBU', use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def echo(update, context):
    context.bot.send_message(update.message.chat_id, text=update.message.text)

def classify(update, context):
    photos = update.message.photo 
    photo_id = photos[-1].file_id
    photo = context.bot.get_file(photo_id)
    photo_fn = photo.download()
    img = open_image(photo_fn)
    pred_clas, pred_idx, pred_probs = learner.predict(img)
    pred_prob = round(float(pred_probs[int(pred_idx)]), 4) * 100
    context.bot.send_message(chat_id=update.message.chat_id, 
    text=f'Prediction class: {str(pred_clas).capitalize()}\nPrediction probability: {pred_prob}%')
    os.remove(photo_fn)

start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text, echo)
classify_handler = MessageHandler(Filters.photo, classify)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(classify_handler)
updater.start_polling()
