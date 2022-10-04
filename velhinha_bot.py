import telebot
import re
import jogo_velha

theBoard = [' '] * 10
playerLetter, computerLetter = ['X', 'O']
isPlayer = False
gameIsPlaying = False

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


@bot.message_handler(func=lambda m: re.search(r'^[1-9]$', m.text))
def playerMove(message):
    global theBoard
    global playerLetter, computerLetter
    global isPlayer
    global gameIsPlaying

    if gameIsPlaying:
        if isPlayer:
            move = message.text
            print(move)
            jogo_velha.makeMove(theBoard, playerLetter, int(move))
            jogo_velha.drawBoard(theBoard)
            if jogo_velha.isWinner(theBoard, playerLetter):
                jogo_velha.drawBoard(theBoard)
                print('Hooray! You have won the game!')
                gameIsPlaying = False
            else:
                if jogo_velha.isBoardFull(theBoard):
                    jogo_velha.drawBoard(theBoard)
                    print('The game is a tie!')
                    gameIsPlaying = False
                else:
                    isPlayer = False
            velhinhaJoga()


def velhinhaJoga():
    global theBoard
    global playerLetter, computerLetter
    global isPlayer
    global gameIsPlaying
    move = jogo_velha.getComputerMove(theBoard, computerLetter)
    print(move)
    jogo_velha.makeMove(theBoard, computerLetter, move)
    jogo_velha.drawBoard(theBoard)
    if jogo_velha.isWinner(theBoard, computerLetter):
        jogo_velha.drawBoard(theBoard)
        print('The computer has beaten you! You lose.')
        gameIsPlaying = False
    else:
        if jogo_velha.isBoardFull(theBoard):
            jogo_velha.drawBoard(theBoard)
            print('The game is a tie!')
            gameIsPlaying = False
        else:
            isPlayer = True
    print(isPlayer)


@bot.message_handler(commands=['eu', 'vc'])
def init_game(message):
    global theBoard
    global playerLetter, computerLetter
    global isPlayer
    global gameIsPlaying

    playerLetter, computerLetter = ['X', 'O']

    print(message.text)
    if message.text == '/eu':
        isPlayer = False
    else:
        isPlayer = True

    bot.send_message(message.chat.id, 'Vamos começar!!!')

    gameIsPlaying = True
    if not isPlayer:
        velhinhaJoga()


bot.infinity_polling()