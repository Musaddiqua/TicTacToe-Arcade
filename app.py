import streamlit as st

# Set up the page aesthetics
st.set_page_config(page_title="Tic Tac Flow", layout="centered")

# Add custom background CSS and dark glass effect
st.markdown(
    """
    <style>
    /* Background Image */
    body {
        background-image: url("https://i.pinimg.com/736x/47/68/22/4768220eda2bdf16308f85bc566d46f7.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Centered dark board with glassmorphism */
    .stApp {
        background-color: rgba(0, 0, 0, 0.65);
        padding: 2rem;
        border-radius: 20px;
        max-width: 650px;
        margin: auto;
        box-shadow: 0 0 20px rgba(0, 255, 174, 0.3);
    }

    .stButton>button {
        height: 70px;
        width: 70px;
        font-size: 40px !important;
        border-radius: 15px;
        background-color: #1f1f2e;
        color: white;
        border: 2px solid #444;
        transition: all 0.2s ease-in-out;
    }

    .stButton>button:hover {
        border: 2px solid #00ffae;
        color: #00ffae;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if 'board' not in st.session_state:
    st.session_state.board = [0] * 9
if 'player' not in st.session_state:
    st.session_state.player = -1

winning_combinations = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]

def analyse_board(board):
    for combo in winning_combinations:
        if board[combo[0]] != 0 and board[combo[0]] == board[combo[1]] == board[combo[2]]:
            return board[combo[0]]
    return 0

def minmax(board, player):
    winner = analyse_board(board)
    if winner != 0:
        return winner * player
    pos = -1
    value = -2
    for i in range(9):
        if board[i] == 0:
            board[i] = player
            score = -minmax(board, -player)
            board[i] = 0
            if score > value:
                value = score
                pos = i
    if pos == -1:
        return 0
    return value

def computer_turn():
    board = st.session_state.board
    pos = -1
    value = -2
    for i in range(9):
        if board[i] == 0:
            board[i] = 1
            score = -minmax(board, -1)
            board[i] = 0
            if score > value:
                value = score
                pos = i
    if pos != -1:
        board[pos] = 1

def check_game_state():
    winner = analyse_board(st.session_state.board)
    if winner != 0:
        if winner == -1:
            st.balloons()
            st.markdown("### 🎉 **You win, legend!** 😎")
        else:
            st.markdown("### 😵 **You lost! The bot reigns supreme.**")
        return True
    elif 0 not in st.session_state.board:
        st.markdown("### 🤝 **It’s a draw! Great battle.**")
        return True
    return False

def reset_game():
    st.session_state.board = [0] * 9
    st.session_state.player = -1

# ✨ Game Title
st.markdown("<h1 style='text-align:center; color:#00ffae;'>✨ Tic Tac Flow</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:lightgray;'>Unleash your inner strategist. ❌ vs 🟢</p>", unsafe_allow_html=True)
st.divider()

# Game Grid UI
cols = st.columns(3)
for i in range(9):
    with cols[i % 3]:
        symbol = "❌" if st.session_state.board[i] == -1 else ("🟢" if st.session_state.board[i] == 1 else " ")
        if symbol == " ":
            if st.button(" ", key=i):
                st.session_state.board[i] = -1
                if not check_game_state():
                    computer_turn()
                    check_game_state()
        else:
            st.button(symbol, key=i, disabled=True)

st.divider()
st.button("🔄 Play Again", on_click=reset_game)
