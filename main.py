from flask import Flask, render_template_string

app = Flask(__name__)


@app.route('/')
def index():
    return render_template_string(
        '''
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Уран — Прототип мессенджера</title>
  <link rel="preconnect" href="https://cdnjs.cloudflare.com" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" />
  <style>
    :root {
      --bg: #f4f5f8;
      --panel: #ffffff;
      --muted: #7a7f8c;
      --border: #e7e8ee;
      --shadow: 0 8px 24px rgba(16, 24, 40, 0.08);
      --primary: #7e3ff2;
      --primary-soft: #8c52ff;
      --msg-them: #eceef3;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      font-family: Arial, sans-serif;
      background: var(--bg);
      color: #141821;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }

    .app {
      width: min(1200px, 100%);
      height: min(820px, calc(100vh - 40px));
      background: var(--panel);
      border-radius: 18px;
      box-shadow: var(--shadow);
      overflow: hidden;
      display: grid;
      grid-template-columns: 350px 1fr;
      border: 1px solid var(--border);
    }

    .sidebar {
      border-right: 1px solid var(--border);
      background: #fbfbfd;
      display: flex;
      flex-direction: column;
      padding: 16px;
      gap: 12px;
    }

    .search-wrap {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .search {
      width: 100%;
      border: 1px solid var(--border);
      background: #fff;
      border-radius: 12px;
      padding: 11px 14px;
      font-size: 14px;
      color: #222;
    }

    .settings-btn {
      border: 1px solid var(--border);
      background: #fff;
      border-radius: 12px;
      width: 42px;
      height: 42px;
      display: grid;
      place-items: center;
      color: #60657a;
      cursor: pointer;
      transition: 0.2s;
    }

    .settings-btn:hover { background: #f2f4fa; }

    .chat-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
      overflow-y: auto;
      padding-right: 4px;
    }

    .chat-item {
      border: 1px solid transparent;
      border-radius: 14px;
      padding: 10px;
      display: grid;
      grid-template-columns: 44px 1fr auto;
      gap: 10px;
      align-items: center;
      cursor: pointer;
      transition: 0.2s;
    }

    .chat-item:hover, .chat-item.active {
      background: #fff;
      border-color: var(--border);
      box-shadow: 0 3px 12px rgba(0, 0, 0, 0.04);
    }

    .avatar {
      width: 44px;
      height: 44px;
      border-radius: 50%;
      display: grid;
      place-items: center;
      color: #fff;
      font-weight: bold;
      font-size: 14px;
    }

    .chat-meta {
      min-width: 0;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .chat-name { font-weight: 700; font-size: 14px; }

    .chat-last {
      color: var(--muted);
      font-size: 13px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 190px;
    }

    .chat-time {
      color: var(--muted);
      font-size: 12px;
      align-self: start;
      margin-top: 2px;
    }

    .chat-panel {
      display: grid;
      grid-template-rows: auto 1fr auto;
      background: #fff;
    }

    .chat-header {
      padding: 14px 20px;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }

    .chat-user {
      display: flex;
      align-items: center;
      gap: 12px;
      font-weight: 700;
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 8px;
      position: relative;
    }

    .icon-btn {
      border: 1px solid var(--border);
      background: #fff;
      color: #4e5466;
      width: 38px;
      height: 38px;
      border-radius: 10px;
      cursor: pointer;
      font-size: 16px;
    }

    .icon-btn:hover { background: #f3f5fb; }

    .menu {
      position: absolute;
      right: 0;
      top: 46px;
      border: 1px solid var(--border);
      background: #fff;
      border-radius: 10px;
      box-shadow: var(--shadow);
      min-width: 150px;
      padding: 6px;
      display: none;
      z-index: 9;
    }

    .menu.open { display: block; }

    .menu button {
      width: 100%;
      border: 0;
      background: transparent;
      text-align: left;
      padding: 10px;
      border-radius: 8px;
      cursor: pointer;
      color: #a02727;
      font-weight: 600;
    }

    .menu button:hover { background: #fff2f2; }

    .messages {
      padding: 18px 20px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 14px;
      background: linear-gradient(180deg, #fff, #fbfbfe);
    }

    .message-row {
      display: flex;
      align-items: flex-end;
      gap: 8px;
      max-width: 80%;
    }

    .message-row.them { align-self: flex-start; }
    .message-row.us { align-self: flex-end; flex-direction: row-reverse; }

    .bubble {
      border-radius: 16px;
      padding: 10px 12px;
      font-size: 14px;
      line-height: 1.4;
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
    }

    .them .bubble { background: var(--msg-them); color: #151823; }
    .us .bubble { background: var(--primary); color: #fff; }

    .msg-avatar {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      display: grid;
      place-items: center;
      color: #fff;
      font-size: 12px;
      font-weight: 700;
      flex-shrink: 0;
    }

    .media.photo {
      width: 170px;
      height: 120px;
      border-radius: 12px;
      background: #d3d7e3;
      display: grid;
      place-items: center;
      color: #3f4558;
      font-weight: 700;
    }

    .video-circle {
      width: 142px;
      height: 142px;
      border-radius: 50%;
      background: #111;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      color: #fff;
      gap: 8px;
    }

    .video-circle i { font-size: 22px; }

    .chat-input {
      border-top: 1px solid var(--border);
      padding: 14px 20px;
      background: #fff;
    }

    .chat-input input {
      width: 100%;
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 12px 14px;
      background: #f7f8fc;
      color: #7b7f90;
      font-size: 14px;
    }

    @media (max-width: 900px) {
      .app { grid-template-columns: 1fr; height: auto; }
      .sidebar { border-right: 0; border-bottom: 1px solid var(--border); }
      .chat-last { max-width: 100%; }
    }
  </style>
</head>
<body>
  <main class="app">
    <aside class="sidebar">
      <div class="search-wrap">
        <input class="search" type="text" placeholder="Поиск или новый чат" />
        <button class="settings-btn" aria-label="Настройки">
          <i class="fa-solid fa-gear"></i>
        </button>
      </div>

      <section class="chat-list">
        <article class="chat-item active">
          <div class="avatar" style="background:#7E3FF2;">AL</div>
          <div class="chat-meta">
            <div class="chat-name">Алина</div>
            <div class="chat-last">Привет! Готова показать новый дизайн.</div>
          </div>
          <time class="chat-time">09:21</time>
        </article>

        <article class="chat-item">
          <div class="avatar" style="background:#22A06B;">МК</div>
          <div class="chat-meta">
            <div class="chat-name">Михаил</div>
            <div class="chat-last">Ок, отправлю документы чуть позже.</div>
          </div>
          <time class="chat-time">Вчера</time>
        </article>

        <article class="chat-item">
          <div class="avatar" style="background:#D97706;">KT</div>
          <div class="chat-meta">
            <div class="chat-name">Катя</div>
            <div class="chat-last">Не забудь про встречу в 14:00 🙌</div>
          </div>
          <time class="chat-time">Пн</time>
        </article>

        <article class="chat-item">
          <div class="avatar" style="background:#0EA5E9;">DV</div>
          <div class="chat-meta">
            <div class="chat-name">Дмитрий</div>
            <div class="chat-last">Видео уже в обработке, скоро пришлю.</div>
          </div>
          <time class="chat-time">Сб</time>
        </article>
      </section>
    </aside>

    <section class="chat-panel">
      <header class="chat-header">
        <div class="chat-user">
          <div class="avatar" style="background:#7E3FF2;">AL</div>
          <span>Алина</span>
        </div>

        <div class="header-actions">
          <button class="icon-btn" aria-label="Видеозвонок">📹</button>
          <button class="icon-btn" aria-label="Аудиозвонок">📞</button>
          <button id="menuToggle" class="icon-btn" aria-label="Меню">⋮</button>
          <div id="chatMenu" class="menu">
            <button id="deleteChat">Удалить чат</button>
          </div>
        </div>
      </header>

      <div class="messages">
        <div class="message-row them">
          <div class="msg-avatar" style="background:#7E3FF2;">AL</div>
          <div class="bubble">Привет! Смотри, как выглядит наш прототип "Уран".</div>
        </div>

        <div class="message-row us">
          <div class="msg-avatar" style="background:#6C2AE0;">US</div>
          <div class="bubble">Очень круто! Есть ли превью с медиа?</div>
        </div>

        <div class="message-row them">
          <div class="msg-avatar" style="background:#7E3FF2;">AL</div>
          <div class="bubble"><div class="media photo">Фото</div></div>
        </div>

        <div class="message-row us">
          <div class="msg-avatar" style="background:#6C2AE0;">US</div>
          <div class="bubble">
            <div class="video-circle">
              <i class="fa-solid fa-play"></i>
              <span>Видео</span>
            </div>
          </div>
        </div>

        <div class="message-row them">
          <div class="msg-avatar" style="background:#7E3FF2;">AL</div>
          <div class="bubble">Если нужно, могу добавить ещё темы оформления.</div>
        </div>
      </div>

      <footer class="chat-input">
        <input type="text" placeholder="Написать сообщение..." disabled />
      </footer>
    </section>
  </main>

  <script>
    const menuToggle = document.getElementById('menuToggle');
    const chatMenu = document.getElementById('chatMenu');
    const deleteChat = document.getElementById('deleteChat');

    menuToggle.addEventListener('click', () => {
      chatMenu.classList.toggle('open');
    });

    deleteChat.addEventListener('click', () => {
      chatMenu.classList.remove('open');
      alert('Чат удален');
    });

    document.addEventListener('click', (event) => {
      if (!chatMenu.contains(event.target) && event.target !== menuToggle) {
        chatMenu.classList.remove('open');
      }
    });
  </script>
</body>
</html>
        '''
    )


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=998, debug=False)
