import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="AI ライティングツール",
    page_icon="✍️",
    layout="wide",
)

# --- API 初期化 ---
if "OPENAI_API_KEY" not in st.secrets:
    st.error("APIキーが設定されていません。`.streamlit/secrets.toml` に OPENAI_API_KEY を設定してください。")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def generate(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


# --- サイドバー ---
st.sidebar.title("✍️ AI ライティングツール")
st.sidebar.markdown("---")
tool = st.sidebar.radio(
    "ツールを選択",
    [
        "📝 ブログ記事作成",
        "📧 メール返信文作成",
        "📋 文章要約",
        "🔍 文章校正・改善",
        "📱 SNS投稿文作成",
        "🎨 文体変換",
        "💡 タイトル生成",
    ],
)

# --- 各ツール ---

if tool == "📝 ブログ記事作成":
    st.title("📝 ブログ記事作成")
    st.caption("テーマを入力するだけで、構成付きのブログ記事を生成します。")

    topic = st.text_input("テーマ・タイトル", placeholder="例：生成AIで仕事の効率を3倍にする方法")
    keywords = st.text_input("含めたいキーワード（任意・カンマ区切り）", placeholder="例：生成AI, 業務効率化, ChatGPT")

    col1, col2, col3 = st.columns(3)
    with col1:
        audience = st.selectbox("ターゲット読者", ["一般向け", "ビジネスパーソン", "専門家", "初心者"])
    with col2:
        tone = st.selectbox("文体", ["です・ます調", "だ・である調", "カジュアル"])
    with col3:
        length = st.selectbox("文章量", ["短め（約500字）", "標準（約1000字）", "長め（約2000字）"])

    if st.button("記事を生成", type="primary", use_container_width=True):
        if not topic:
            st.warning("テーマを入力してください。")
        else:
            length_map = {"短め（約500字）": "500字程度", "標準（約1000字）": "1000字程度", "長め（約2000字）": "2000字程度"}
            prompt = f"""以下の条件でブログ記事を作成してください。

テーマ：{topic}
ターゲット読者：{audience}
文体：{tone}
文章量：{length_map[length]}
{"含めるキーワード：" + keywords if keywords else ""}

構成のルール：
- 導入文（読者の共感を引く）
- 本文（H2/H3見出しを使って整理）
- まとめ（行動を促す締め）
"""
            with st.spinner("記事を生成中..."):
                result = generate(prompt)
            st.markdown(result)
            st.download_button("テキストをダウンロード", result, file_name="blog_article.txt", use_container_width=True)


elif tool == "📧 メール返信文作成":
    st.title("📧 メール返信文作成")
    st.caption("受け取ったメールを貼り付けると、返信文のドラフトを作成します。")

    original = st.text_area("受け取ったメール", height=180, placeholder="ここに受け取ったメール文を貼り付けてください")
    points = st.text_area("返信で伝えたいこと（任意）", height=80, placeholder="例：来週火曜に打ち合わせ可能、資料は水曜送付予定")

    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox("トーン", ["丁寧・ビジネス", "フレンドリー", "簡潔・端的"])
    with col2:
        relation = st.selectbox("相手との関係", ["取引先・顧客", "上司・目上", "同僚", "友人・知人"])

    if st.button("返信文を生成", type="primary", use_container_width=True):
        if not original:
            st.warning("受け取ったメールを入力してください。")
        else:
            prompt = f"""以下のメールへの返信文を作成してください。

【受け取ったメール】
{original}

【返信で伝えたいこと】
{points if points else "適切に返信してください"}

【トーン】{tone}
【相手との関係】{relation}

件名（Re:〜）から本文・署名欄まで完成形で出力してください。"""
            with st.spinner("返信文を生成中..."):
                result = generate(prompt)
            st.markdown(result)
            st.download_button("テキストをダウンロード", result, file_name="email_reply.txt", use_container_width=True)


elif tool == "📋 文章要約":
    st.title("📋 文章要約")
    st.caption("長い文章を短く整理します。記事・議事録・資料などに。")

    text = st.text_area("要約したい文章", height=280, placeholder="ここに要約したい文章を貼り付けてください")

    col1, col2 = st.columns(2)
    with col1:
        length = st.selectbox("要約の長さ", ["3行以内", "100字以内", "200字以内", "400字以内"])
    with col2:
        style = st.selectbox("出力スタイル", ["文章形式", "箇条書き", "見出し＋要点"])

    if st.button("要約する", type="primary", use_container_width=True):
        if not text:
            st.warning("要約したい文章を入力してください。")
        else:
            prompt = f"""以下の文章を要約してください。

要約の長さ：{length}
出力スタイル：{style}

【文章】
{text}"""
            with st.spinner("要約中..."):
                result = generate(prompt)
            st.markdown(result)
            st.download_button("テキストをダウンロード", result, file_name="summary.txt", use_container_width=True)


elif tool == "🔍 文章校正・改善":
    st.title("🔍 文章校正・改善")
    st.caption("誤字チェックから文章改善まで、モードを選んで実行できます。")

    text = st.text_area("校正・改善したい文章", height=250)
    mode = st.radio(
        "モード",
        ["誤字・脱字チェック", "より自然な文章に改善", "より丁寧な表現に", "よりシンプルに"],
        horizontal=True,
    )

    if st.button("実行する", type="primary", use_container_width=True):
        if not text:
            st.warning("文章を入力してください。")
        else:
            mode_prompts = {
                "誤字・脱字チェック": "誤字・脱字・文法の誤りをすべて修正し、修正箇所と理由を説明してください。",
                "より自然な文章に改善": "文章をより自然で読みやすく改善してください。【改善前】→【改善後】の形式で示してください。",
                "より丁寧な表現に": "文章をより丁寧でフォーマルな表現に変換してください。",
                "よりシンプルに": "文章をよりシンプルで分かりやすい表現に変換してください。難しい言葉は避けてください。",
            }
            prompt = f"""{mode_prompts[mode]}

【文章】
{text}"""
            with st.spinner("処理中..."):
                result = generate(prompt)
            st.markdown(result)
            st.download_button("テキストをダウンロード", result, file_name="proofread.txt", use_container_width=True)


elif tool == "📱 SNS投稿文作成":
    st.title("📱 SNS投稿文作成")
    st.caption("プラットフォームの特性に合わせた投稿文を生成します。")

    topic = st.text_area("投稿したい内容・テーマ", height=100, placeholder="例：生成AIを使って業務効率化に成功した体験談")

    col1, col2, col3 = st.columns(3)
    with col1:
        platform = st.selectbox("プラットフォーム", ["X（Twitter）", "Instagram", "Facebook", "LinkedIn", "note"])
    with col2:
        tone = st.selectbox("トーン", ["プロフェッショナル", "カジュアル", "共感・感情的", "教育的・情報提供"])
    with col3:
        count = st.selectbox("生成パターン数", ["1パターン", "3パターン"])

    hashtag = st.checkbox("ハッシュタグを含める", value=True)

    if st.button("投稿文を生成", type="primary", use_container_width=True):
        if not topic:
            st.warning("投稿したい内容を入力してください。")
        else:
            prompt = f"""{platform}の投稿文を{count}作成してください。

テーマ：{topic}
トーン：{tone}
{"ハッシュタグを含める（5個程度）" if hashtag else "ハッシュタグは不要"}

{platform}の文字数制限・特性（改行・絵文字の使い方）に合わせて作成してください。
複数パターンの場合は【パターン1】【パターン2】のように区切ってください。"""
            with st.spinner("投稿文を生成中..."):
                result = generate(prompt)
            st.markdown(result)
            st.download_button("テキストをダウンロード", result, file_name="sns_post.txt", use_container_width=True)


elif tool == "🎨 文体変換":
    st.title("🎨 文体変換")
    st.caption("文章の意味はそのままに、文体・スタイルだけを変換します。")

    text = st.text_area("変換したい文章", height=200)
    target_style = st.selectbox(
        "変換後の文体",
        [
            "ビジネス文書（フォーマル）",
            "カジュアル・話し言葉",
            "です・ます調",
            "だ・である調",
            "易しい言葉（子どもでも分かる）",
            "英語に翻訳",
            "日本語に翻訳",
        ],
    )

    if st.button("変換する", type="primary", use_container_width=True):
        if not text:
            st.warning("変換したい文章を入力してください。")
        else:
            prompt = f"""以下の文章を「{target_style}」に変換してください。

意味・内容はそのままに、文体だけを変換してください。変換後の文章のみを出力してください。

【元の文章】
{text}"""
            with st.spinner("変換中..."):
                result = generate(prompt)
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("変換前")
                st.text_area("", value=text, height=200, disabled=True, label_visibility="collapsed")
            with col2:
                st.subheader("変換後")
                st.text_area("", value=result, height=200, label_visibility="collapsed")
            st.download_button("変換後テキストをダウンロード", result, file_name="converted.txt", use_container_width=True)


elif tool == "💡 タイトル生成":
    st.title("💡 タイトル生成")
    st.caption("記事の内容から、クリックされやすいタイトル候補を複数生成します。")

    content = st.text_area(
        "記事の内容・概要",
        height=150,
        placeholder="例：生成AIツールを使って営業資料の作成時間を1/3に削減した方法について解説する記事",
    )

    col1, col2 = st.columns(2)
    with col1:
        purpose = st.selectbox("用途", ["ブログ記事", "メルマガ件名", "SNS投稿", "資料・レポート", "YouTube動画タイトル"])
    with col2:
        count = st.select_slider("生成する数", options=[3, 5, 10], value=5)

    styles = st.multiselect(
        "タイトルのスタイル（複数選択可）",
        ["数字を使う", "疑問形", "インパクト重視", "SEO重視", "感情に訴える", "具体的なメリットを示す"],
        default=["数字を使う", "インパクト重視"],
    )

    if st.button("タイトルを生成", type="primary", use_container_width=True):
        if not content:
            st.warning("記事の内容・概要を入力してください。")
        else:
            prompt = f"""{purpose}のタイトルを{count}個生成してください。

【内容・概要】
{content}

【スタイル条件】
{", ".join(styles) if styles else "特に指定なし"}

番号付きリストで出力し、各タイトルの後にひとこと狙いを添えてください。"""
            with st.spinner("タイトルを生成中..."):
                result = generate(prompt)
            st.markdown(result)
            st.download_button("テキストをダウンロード", result, file_name="titles.txt", use_container_width=True)
