import re

import pandas as pd
import plotly.colors as pc
import plotly.express as px
import requests

pfgen_leaderboard_url = "https://raw.githubusercontent.com/pfnet-research/pfgen-bench/refs/heads/main/README.md"
response = requests.get(pfgen_leaderboard_url)
match = re.search(
    r"<!-- leaderboard -->(.*?)<!-- /leaderboard -->",
    response.text,
    re.DOTALL,
)
if match is not None:
    leaderboard_str = match.group(1).strip()
data: dict[str, list[int | float | str]] = {
    "size": [],
    "score": [],
    "model_name": [],
}
unknown_size_data: dict[str, list[float | str]] = {
    "score": [],
    "model_name": [],
}
cleaned_leaderboard_str = re.sub(r"</?code>", "", leaderboard_str)
for line in cleaned_leaderboard_str.split("\n"):
    score_tmp = line.split("|")[2]
    match_score = re.search(r"([0-9\.]+)", score_tmp)
    if match_score is None:
        continue
    score = float(match_score.group(1))
    model_name_part = line.split("|")[3]
    match_model_name_part = re.search(r"\(([^\)]+)", model_name_part)
    if match_model_name_part is None:
        continue
    model_name_tmp = match_model_name_part.group(1)
    if model_name_tmp.split("/")[0] != "result":
        continue
    model_name = "/".join(model_name_tmp.split("/")[1:3])
    match_size = re.search(r"([0-9\.]+)[bB]", line)
    if match_size is None:
        size = None
    else:
        size = float(match_size.group(1))
    if "deepseek-ai/DeepSeek-V3" in model_name:
        size = 685.0
    elif "cyberagent/open-calm-large" in model_name:
        size = 0.83
    elif "cyberagent/open-calm-medium" in model_name:
        size = 0.4
    elif "cyberagent/open-calm-small" in model_name:
        size = 0.16
    elif "microsoft/Phi-3-medium-128k-instruct" in model_name:
        size = 14.0
    elif "microsoft/Phi-3-medium-4k-instruct" in model_name:
        size = 14.0
    elif "microsoft/Phi-3-small-128k-instruct" in model_name:
        size = 7.39
    elif "microsoft/phi-2" in model_name:
        size = 2.78
    elif "microsoft/Phi-3-small-8k-instruct" in model_name:
        size = 7.39
    elif "microsoft/phi-1_5" in model_name:
        size = 1.42
    elif "microsoft/phi-1" in model_name:
        size = 1.42
    elif "mistralai/Mixtral-8x22B-v0.1" in model_name:
        size = 141.0
    elif "mistralai/Mixtral-8x7B-Instruct-v0.1" in model_name:
        size = 46.7
    elif "mistralai/Mixtral-8x7B-v0.1" in model_name:
        size = 46.7
    elif "mistralai/Mistral-Nemo-Base-2407" in model_name:
        size = 12.2
    elif "mistralai/Mistral-Nemo-Instruct-2407" in model_name:
        size = 12.2
    elif "weblab-GENIAC/Tanuki-8x8B-dpo-v1.0" in model_name:
        size = 47.0
    elif "Qwen/Qwen1.5-MoE-A2.7B-Chat" in model_name:
        size = 14.3
    elif "Qwen/Qwen1.5-MoE-A2.7B" in model_name:
        size = 14.3
    elif "CohereForAI/c4ai-command-r-plus" in model_name:
        size = 104.0
    elif "CohereForAI/c4ai-command-r-v01" in model_name:
        size = 35.0
    elif "sbintuitions/tiny-lm-chat" in model_name:
        size = 0.016
    elif "sbintuitions/tiny-lm" in model_name:
        size = 0.016
    elif "karakuri-ai/karakuri-lm-8x7b-instruct-v0.1" in model_name:
        size = 46.7
    elif "pfnet/plamo-1.0-prime" in model_name:
        size = 100.0
    elif "openai" in model_name:
        size = None
    elif size is None and "google" in model_name:
        size = None
    if size is None:
        unknown_size_data["score"].append(score)
        unknown_size_data["model_name"].append(model_name)
        continue
    data["size"].append(size)
    data["score"].append(score)
    data["model_name"].append(model_name)
df = pd.DataFrame.from_dict(data)
fig = px.scatter(
    df,
    x="size",
    y="score",
    color="model_name",
    hover_data=["model_name"],
)
unknown_df = pd.DataFrame.from_dict(unknown_size_data)
colors = pc.qualitative.Plotly
for index, row in unknown_df.sort_values("score").iterrows():
    fig.add_hline(
        y=row["score"],
        line_dash="dash",
        annotation_text=row["model_name"],
        annotation_position="bottom",
        annotation_font=dict(
            color=colors[index % len(colors)],
            size=14,
        ),
        line_color=colors[index % len(colors)],
    )
fig.update_xaxes(range=[0, 700])
fig.update_yaxes(range=[0.597, 0.94])
fig.write_html("pfgen_bench_20250102.html")
fig.show()
