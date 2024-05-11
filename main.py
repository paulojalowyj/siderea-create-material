import os
from openai import OpenAI
from moviepy.editor import VideoFileClip
import os
from dotenv import load_dotenv

load_dotenv()

def process_mp4(mp4_file):
    # Extrair o nome base do arquivo (sem extensão)
    base_name, _ = os.path.splitext(mp4_file)

    # Gerar nomes de arquivos de saída
    mp3_file = f"{base_name} - AUDIO.mp3"
    transcription_file = f"{base_name} - TRANSCRICAO.txt"
    material_file = f"{base_name} - MATERIAL COMPLEMENTAR.txt"

    # Extrair áudio
    video_clip = VideoFileClip(mp4_file)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(mp3_file, bitrate="24k")
    audio_clip.close()
    video_clip.close()
    print(f"Áudio extraído de {mp4_file}")

    # Transcrição
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )  # Substitua pela sua chave API
    with open(mp3_file, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", file=audio_file, response_format="text"
        )
    with open(transcription_file, "w") as f:
        f.write(transcription)
    print(f"Transcrição salva em {transcription_file}")

    # Produção de material complementar
    content_title = (
        "Lei Geral de Proteção de Dados"  # Substitua pelo título do seu conteúdo
    )

    with open(transcription_file, "r") as f:
        text = f.read()

    context_prompt = (
        "Você é um especialista em produção de materiais para ensino à distancia. "
        "O seu contexto de trabalho é o texto abaixo, ele foi retirado da transcrição da aula de um curso sobre "
        + content_title
        + "\n\nSeu contexto base é: \n"
        + text
    )

    # Chamadas de API OpenAI para gerar seções do material (título, introdução, etc.)
    # Solicitação da API
    titulo = client.chat.completions.create(
        model=os.getenv("OPENAI_GPT_MODEL"),
        messages=[
            {
                "role": "system",
                "content": context_prompt + text,
            },
            {
                "role": "user",
                "content": "Crie um título para o material com base no conteúdo da transcrição que trabalhamos hoje.",
            },
        ],
        max_tokens=4096,
    )

    introducao = client.chat.completions.create(
        model=os.getenv("OPENAI_GPT_MODEL"),
        messages=[
            {"role": "system", "content": context_prompt},
            {
                "role": "user",
                "content": "Elabore uma sinopse de 1 parágrafo, com no mínimo 3 frases, sobre o conteúdo;",
            },
        ],
        max_tokens=4096,
    )

    conteudo1 = client.chat.completions.create(
        model=os.getenv("OPENAI_GPT_MODEL"),
        messages=[
            {"role": "system", "content": context_prompt},
            {
                "role": "user",
                "content": "Aborde os principais tópicos da aula em um texto de resumo do conteúdo, não utilize tópicos, elabore pelo menos 7 parágrafos de texto, cada parágrafo com no mínimo 3 frases;",
            },
        ],
        max_tokens=4096,
    )

    conteudo2 = client.chat.completions.create(
        model=os.getenv("OPENAI_GPT_MODEL"),
        messages=[
            {"role": "system", "content": context_prompt},
            {
                "role": "user",
                "content": "Elabore uma lista com 5 tópicos explicando termos relevantes em relação ao conteúdo abordado. Para cada tópico utilize 1 parágrafo com pelo menos 3 frases;",
            },
        ],
        max_tokens=4096,
    )

    conteudo3 = client.chat.completions.create(
        model=os.getenv("OPENAI_GPT_MODEL"),
        messages=[
            {"role": "system", "content": context_prompt},
            {
                "role": "user",
                "content": "Adicione 3 referências externas ao material, se possivel referências em português do Brasil. Elabore um parágrafo para cada referência, explicando seu contexto em relação ao conteúdo;",
            },
        ],
        max_tokens=4096,
    )

    conteudo4 = client.chat.completions.create(
        model=os.getenv("OPENAI_GPT_MODEL"),
        messages=[
            {"role": "system", "content": context_prompt},
            {
                "role": "user",
                "content": "Adicione 1 referência de vídeo sobre assunto abordado na aula, seguida de um breve resumo do conteúdo do vídeo, o resumo deve ter 1 parágrafo de 3 frases;",
            },
        ],
        max_tokens=4096,
    )

    conteudo5 = client.chat.completions.create(
        model=os.getenv("OPENAI_GPT_MODEL"),
        messages=[
            {"role": "system", "content": context_prompt},
            {
                "role": "user",
                "content": "Adicione 1 referência em formato podcast sobre o assunto abordado na aula, seguida de um breve resumo do conteúdo do podcast, o resumo deve ter 1 parágrafo de 3 frases;",
            },
        ],
        max_tokens=4096,
    )

    conclusao = client.chat.completions.create(
        model=os.getenv("OPENAI_GPT_MODEL"),
        messages=[
            {"role": "system", "content": context_prompt},
            {
                "role": "user",
                "content": "Elabore uma conclusão de 2 parágrafos sobre conteúdo abordado, cada parágrafo com no mínimo 3 frases.",
            },
        ],
        max_tokens=4096,
    )

    questoes = client.chat.completions.create(
        model=os.getenv("OPENAI_GPT_MODEL"),
        messages=[
            {"role": "system", "content": context_prompt},
            {
                "role": "user",
                "content": "Crie 5 questões com base no conteúdo da transcrição. Elabore 5 respostas para cada questão, sendo quatro respostas incorretas e uma correta para cada questão. Nas chamadas para as respostas utilize a), b), c), d) e e) nas 5 questões. Ao final das opções, adicione a alternativa correta.",
            },
        ],
        max_tokens=4096,
    )

    # Texto expandido gerado pelo ChatGPT
    result_titulo = titulo.choices[0].message.content
    result_introducao = introducao.choices[0].message.content
    result_conteudo1 = conteudo1.choices[0].message.content
    result_conteudo2 = conteudo2.choices[0].message.content
    result_conteudo3 = conteudo3.choices[0].message.content
    result_conteudo4 = conteudo4.choices[0].message.content
    result_conteudo5 = conteudo5.choices[0].message.content
    result_conclusao = conclusao.choices[0].message.content
    result_questoes = questoes.choices[0].message.content

    # Escrever o material complementar no arquivo
    with open(material_file, "w") as f:
        f.write("Título: \n")
        f.write(result_titulo)
        f.write("\n\nSinopse: \n")
        f.write(result_introducao)
        f.write("\n\nCapsula de conteúdo: \n")
        f.write(result_conteudo1)
        f.write("\n\nGlossário: \n")
        f.write(result_conteudo2)
        f.write("\n\nConclusão: \n")
        f.write(result_conclusao)
        f.write("\n\nReferências: \n")
        f.write(result_conteudo3)
        f.write("\n\nVídeo Complementar: \n")
        f.write(result_conteudo4)
        f.write("\n\nPodcast: \n")
        f.write(result_conteudo5)
        f.write("\n\nQuestões: \n")
        f.write(result_questoes)

    print(f"Material complementar gerado em {material_file}")


# Processar todos os arquivos .mp4 na pasta atual
for filename in sorted(os.listdir(".")):
    if filename.endswith(".mp4"):
        process_mp4(filename)
