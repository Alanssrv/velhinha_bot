import telebot

bot = telebot.TeleBot("TOKEN", parse_mode = None)

@bot.message_handler(commands=['start', 'menu'])
def command_start(message):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    start_markup.row('/menu', '/ajuda')
    start_markup.row('/sobre', '/jogar')
    bot.send_message(message.chat.id, "👵🏽 Olá, eu sou a Velhinha!\nQuer /ajuda de como jogar o jogo da velha?\nClique em /sobre para saber sobre mim")
    bot.send_message(message.chat.id, "Para iniciar uma partida contra a Velhinha, clique em /jogar")
    bot.send_message(message.from_user.id, "Utilize o atalho rápido!\n⌨ Você pode /utilizar_teclado se preferir", reply_markup=start_markup)
    

@bot.message_handler(commands=['ajuda'])
def help(message):
    bot.send_message(message.chat.id, "O jogo da velha ou jogo do galo ou três em linha é um jogo e/ou passatempo popular.\nÉ um jogo de regras extremamente simples, que não traz grandes dificuldades para seus jogadores e é facilmente aprendido.")
    bot.send_message(message.chat.id, "No modo básico do jogo, participam duas pessoas, que jogam alternadamente, preenchendo cada um dos\nespaços vazios. Cada participante poderá usar um símbolo (❌ ou ⭕). Vence o jogador que conseguir\nformar primeiro uma linha com três símbolos iguais, seja ela na horizontal, vertical ou diagonal.")
    

@bot.message_handler(commands=['sobre'])
def about(message):
    bot.send_message(message.chat.id, "Eu sou a Velhinha, uma IA desenvolvida para te desafiar no Jogo da Velha, minha especialidade.\nFui desenvolvida com @BotFather e Python 🐍, por @alanssrv",)


@bot.message_handler(commands=['utilizar_teclado'])
def command_hide(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "⌨...", reply_markup=hide_markup)


@bot.message_handler(commands=['jogar'])
def change_player(message):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    start_markup.row('/eu', '/vc')
    bot.send_message(message.chat.id, "Escolha quem começa jogando\n/eu (a Velhinha) ⭕\n/vc ❌")

@bot.message_handler(commands=['eu', 'jogar'])
def init_game(message):
    bot.send_message(message.chat.id, 'Vamos começar!!!')
    
bot.infinity_polling()