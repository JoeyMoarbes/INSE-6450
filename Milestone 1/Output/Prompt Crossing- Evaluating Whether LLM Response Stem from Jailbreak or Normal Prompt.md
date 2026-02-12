## Prompt Crossing: Evaluating Whether LLM Response Stem from Jailbreak or Normal Prompt

Kyungho Kim ActionPower Seoul, South Korea kyungho.kim@actionpower.kr

Jaejin Seo ActionPower Seoul, South Korea jaejin.seo@actionpower.kr

Seongmin Park ActionPower Seoul, South Korea seongmin.park@actionpower.kr

Jihwa Lee ActionPower Seoul, South Korea jihwa.lee@actionpower.kr

Abstract -The evolution of Large Language Models (LLMs) has sparked growing concerns about jailbreak, crafted prompts that bypass safety guardrails and lead to the generation of harmful information. While recent research primarily focuses on identifying harmful content within LLM outputs, limited attention has been paid to detecting jailbreak intent directly from user prompts. This paper proposes a novel framework, called Prompt-Crossing, for analyzing user prompts and identifying those harboring potential jailbreak intent based on the response of LLM. Moreover, while existing methods determine jailbreak intent by looking at whether the response of LLM contains harmful information, our proposed framework can determine whether the user prompt, triggering the response of LLM, has jailbreak intent even if the response does not contain harmful information. In addition, our method performs filtering based on the likelihood calculated in a forward-step manner, deviates from traditional inference-based LLM usage, demonstrating a new application for LLMs. To demonstrate our proposed framework, we achieve state-of-the-art on the AdvBench benchmark using two LLMs, LLAMA and Falcon.

Index Terms -Jailbreak, LLM, Filtering, Safety

## I. INTRODUCTION

Large Language Models (LLMs) have shown promising results across various fields within Natural Language Processing (NLP), such as search [14], conversation [6], and information retrieval [16]. This advancement has sparked considerable interest both academically and socially. From an academic perspective, open-source LLMs such as LLAMA [12], LLAMA2 [13], Vicuna [4], and Falcon [1] are rapidly developed. From a social perspective, the services that make LLMs available to the public, starting notably with ChatGPT [8], have attracted significant attention from individuals and corporations alike. This trend is evident in the swift development and public release of large-scale corporate LLMs such as Google Gemini [11] and Anthropic Claude [2].

The unprecedented interest in and rapid performance improvements of Large Language Models (LLMs) have inadvertently led to the relative overlooking of potential risks. LLMs operate by pre-training lots of knowledge and generating appropriate follow-up text for any given input. While extensive knowledge acquisition enables LLMs to possess a wealth of pre-knowledge and respond to diverse user demands, it also implies a risk that LLMs operate as unintentionally. In other words, accessing an unrefined text corpus can cause LLMs to generate illegal, harmful, or toxic content for users.

There are several existing efforts to prevent LLM from generating harmful content. For example, RLHF [9] reduces the proportion of toxic responses by applying reinforcement learning to fine-tuned LLMs to produce more human-preferred responses. However, it remains challenging to fully control the output of probabilistic generative models to eliminate the toxic content [5]. Moreover, there are attempts to circumvent the safety filters of LLMs for malicious purposes. These methods of bypassing LLMs safety guardrail are known as jailbreaks [7, 15]. Using these jailbreak prompts, it is possible to bypass the safety filters of LLMs and force the model to generate unethical, immoral, illegal, or toxic responses. Therefore, in addition to developing techniques to prevent LLM from generating toxic responses, additional validation is crucial for ensuring that the final output is not toxic when deploying LLM for practical use.

Several methods exist to determine whether the final output has harmful content. The first is to instruct the LLMs to perform an illegal action while simultaneously specifying the first sentence of its response [17]. This lexical approach allows us to assess whether the jailbreak is successful by examining the initial sentence of the response of LLM. The second method uses different LLM to determine whether a response contains toxic elements or not [3, 10]. This semantic approach evaluates the overall harmfulness of the response. However, both of the aforementioned methods have limitations. The lexical approach relies on the first sentence of the response to determine the success of the jailbreak. However, the LLM can generate harmful content even if the initial sentence does not match the specified sentence. Utilizing different LLMs to assess the harmfulness of the response requires additional training for toxicity detection. Additionally, the inherent safety filters embedded within LLMs may lead to an unconditional aversion to handling toxic content, potentially hindering accurate assessments. In addition, the methods mentioned above only focus on whether the response contains harmful content. Therefore, those cannot determine whether the user prompt actually intends to perform a jailbreak. For example, a malicious user asks an illegal question using a prompt with jailbreak intent, but the response may not contain harmful content due to the safety filter. In this case, existing methodologies cannot determine whether the user prompt has jailbreak intent.

To overcome the limitations of the aforementioned ap-

Fig. 1: Overall framework of Prompt-Crossing.

<!-- image -->

proaches, we propose a framework called prompt-crossing . It estimates the probability that the response is generated from a set of known prompts, including both normal and jailbreak prompts. This approach can inform whether the unseen user prompt is closer to jailbreak or common prompt where the safety filter is normally applied. Moreover, unlike conventional LLM usage, which generates new responses through inference over a long time, our approach leverages the characteristics of the forward step of the training stage to calculate the likelihood of user-generated texts based on known prompt sets within a short time. This novel filtering method performs filtering based on the likelihood calculated in a forward-step manner, deviates from traditional inference-based LLM usage, demonstrating a new application for LLMs. The efficiency of our proposed method is demonstrated by the AdvBench benchmark [17], which is widely used in jailbreak simulation. Furthermore, our proposed framework is applicable across multiple LLMs while demonstrating superior performance compared to the robust baseline, GPT-4.

In conclusion, we address the issues of existing approaches in a practical and straightforward manner, resulting in the more effective detection of jailbreak intent in user prompt. Our main contributions include:

- We propose a novel framework, called Prompt-Crossing , to determine if the user prompt has jailbreak intent, even if the response of LLM does not contain harmful content.
- We validate the efficacy of Prompt-Crossing by showing better performance than GPT-4 on AdvBench benchmark.
- We validate our approach using various LLM models and provide a detailed analysis.

Fig. 2: The example of getting response of model based on user prompt and question.

<!-- image -->

## II. SYSTEM FRAMEWORK

The Figure 1 shows the overview of proposed framework, including general LLM framework. The Prompt-Crossing framework (Figure 1) comprises two components: Checker Prompts and Jailbreak Checker . The Figure 2 shows example of a general LLM framework generating response based on both user question U q and user prompt U p .

Checker Prompts are a set of prompts C { N,J } p that are a collection of both normal N and jailbreak J prompts that are widely known in advance. The Figure 3 provides actual prompt examples of checker prompts. Jailbreak Checker utilizes the Checker Prompts C { N,J } p , victim LLM response R , and User Question U q as inputs to judge LLM. Based on the given input data, judge LLM L j calculates the probability distribution that the judge LLM will generate the same response R from the

Fig. 3: The checker prompts ( left : normal, right : jailbreak)

<!-- image -->

victim LLM L v . It calculates whether the response is more likely to come from the set of normal prompts or the set of jailbreak prompts to determine whether the user prompt has jailbreak intent or not. For consistency of the experiment, we define the input using the same template for each of victim LLM and judge LLM. The template used for victim LLM is ' { user prompt } { user question } ', and the template used for judge LLM is ' { checker prompt } { user question } Answer: { response } '. The above process can be represented as follows:

<!-- formula-not-decoded -->

where P { N,J } refers to the probability that user prompt is normal N or jailbreak J type.

The figure 4 displays the obtained results when executing the entire Prompt-Crossing framework. It illustrates the potential of a user prompt actually containing jailbreak intention, based solely on the user question and the model response, without the user prompt. This potential is calculated by averaging the likelihood probabilities derived from the normal checker prompts and jailbreak checker prompts collected beforehand. In detail, the score is obtained by comparing whether the given model response is more likely to occur with the combination of the given user question and normal checker prompts or with the combination of the user question and jailbreak checker prompts. This score is measured based on the average likelihood probability of the response occurring when both the user question and checker prompts are provided to the judge LLM.

## III. EXPERIMENTS

Experiment Setting. Promt-Crossing is evaluated on the 'harmful behaviors' subset of the AdvBench benchmark [17]

Fig. 4: Demonstration of Prompt-Crossing framework.

<!-- image -->

as the same setting used in [3]. The response from the victim LLM is collected using GPT-3.5. To compare our proposal framework with the existing approach, the most powerful models, GPT-3.5 and GPT-4, are used as the baseline. In order to perform the task of determining whether the user prompt is jailbreak to GPT, the following prompt template is used: ' Is the given response an answer to a question (jailbreak) that bypasses the model's safety filter? Answer: [Yes, No] Response: { Response } '. In addition, to prove that

TABLE I: The result of Prompt-Crossing. v1 means using LLAMA-27B as judge LLM and v2 means using Falcon-7B as judge LLM. Bold with underline means best performance. Bold means the second best.

|                | Accuaracy   | Accuaracy   | Accuaracy   | Accuaracy   |
|----------------|-------------|-------------|-------------|-------------|
| User Prompt    | GPT-3.5     | GPT-4       | Ours(v1)    | Ours(v2)    |
| RAW            | 0.26        | 0.30        | 0.54        | 0.84        |
| LLAMA          | 0.32        | 0.30        | 0.3         | 0.74        |
| PLUS           | 0.34        | 0.38        | 0.64        | 0.84        |
| VICUNA         | 0.22        | 0.24        | 0.42        | 0.78        |
| GPT            | 0.28        | 0.26        | 0.52        | 0.88        |
| Normal Avg.    | 0.284       | 0.296       | 0.484       | 0.816       |
| AIM            | 0.30        | 0.30        | 1.0         | 0.98        |
| DEV            | 0.90        | 0.90        | 0.76        | 0.64        |
| DAN            | 0.40        | 0.40        | 0.92        | 0.58        |
| EVIL           | 0.48        | 0.52        | 0.88        | 0.68        |
| ANTI           | 0.66        | 0.70        | 0.68        | 0.5         |
| Jailbreak Avg. | 0.548       | 0.564       | 0.848       | 0.676       |
| Total Avg.     | 0.416       | 0.430       | 0.666       | 0.746       |

our proposed framework is generally applicable, two different LLMs, LLAMA 1 and FALCON 2 , are utilized as judge LLMs. The Checker Prompts consist of 5 normal prompts and 5 jailbreak prompts. The normal prompts are the same as in [3]. The jailbreak prompts are composed of the five highest ranked prompts in website 3 4 . Cross entropy loss is utilized to quantify the probability distribution of the LLM response. More details are available at https://youtu.be/wivRaoFwIHs .

Experiment Result. Table I shows the accuracy of the baseline and proposed framework. Regardless of which model is utilized as the judge LLM, our proposed framework outperforms the baseline. In both cases where the intent of the user prompt is normal or jailbreak, our approach makes more accurate predictions than the baseline.

|             | Prompt Crossing (Checker)   | Prompt Crossing (Checker)   |
|-------------|-----------------------------|-----------------------------|
| User Prompt | Normal                      | Jailbreak                   |
| Normal      | 10.88                       | 11.09                       |
| Jailbreak   | 11.34                       | 11.28                       |

TABLE II: The cross-entropy loss of each combination of user prompt and checker prompt.

Result Analysis. Table II shows the cross-entropy loss based on the combination of the type of user prompt and checker prompt. Our analysis reveals that the combination of user prompt and checker prompt achieves lower cross-entropy loss when paired with prompts of the same type (normal-

1 huggingface.co/meta-llama/Llama-2-7b

2 huggingface.co/tiiuae/falcon-7b

3 www.jailbreakchat.com

4 Unfortunately, the website is no longer supported. However, the detail information of used prompts are available in the provided demo video or in the rubend18/ChatGPT-Jailbreak-Prompts dataset on Hugging Face.

normal and jailbreak-jailbreak) compared to heterogeneous pairings (normal-jailbreak and jailbreak-normal).

Figure 5 provides more detailed information about each combination of prompts that make up the user and checker prompts. Each row in the heatmap is normalized to a normal distribution. The heatmap depicts cross-entropy loss for various combination, where each row corresponds to user prompt. Rows 1-5 represent scenarios where the user prompt is the normal type. Within these rows, the upper-left 5x5 sub-matrix exhibits lower cross-entropy loss(green) compared to the upper-right sub-matrix. Notably, employing the AIM and DEV jailbreak prompts as checker prompts (Column 67) in the upper-right sub-matrix leads to significantly higher cross-entropy loss (red). The bottom five rows depict scenarios where the user prompt harbors jailbreak intent. In these rows, employing the DAN as the checker prompt (Column 8) yields remarkably low cross-entropy loss (green).

<!-- image -->

Checker Prompts

Fig. 5: The heatmap of cross-entropy loss of each prompt combination. The x-axis and y-axis represent the checker prompts and the user prompts, respectively.

## IV. CONCLUSION

This paper introduces Prompt-Crossing , a novel framework designed to detect jailbreak intent in user prompt, overcoming the limitations of conventional safety filters that solely investigate LLM response for harmful content. To achieve this, Prompt-Crossing leverages pre-known sets of normal and jailbreak prompts and calculate the generation probability of the response of victim LLM based on each set. This enables us to move beyond mere output verification and unveil the true intent behind the triggering prompt. This method enables us to determine the actual intent of the user prompt that triggered the response of LLM. The efficacy of proposed approach is validated through on AdvBench, a widely used jailbreak benchmark. Notably, Prompt-Crossing surpasses the performance of a robust baseline, GPT-4, while simultaneously demonstrating its scalability by utilizing diverse LLMs. We hope that our framework opens new possibilities in safety guidelines for jailbreak.

## REFERENCES

- [1] E. Almazrouei, H. Alobeidli, A. Alshamsi, A. Cappelli, R. Cojocaru, M. Debbah, ´ Etienne Goffinet, D. Hesslow, J. Launay, Q. Malartic, D. Mazzotta, B. Noune, B. Pannier, and G. Penedo. The falcon series of open language models.
- [2] Anthropic. Anthropic ai: Model card and evaluations for claude models. https://www-files.anthropic.com/production/images/ Model-Card-Claude-2.pdf, 2023.
- [3] P. Chao, A. Robey, E. Dobriban, H. Hassani, G. J. Pappas, and E. Wong. Jailbreaking black box large language models in twenty queries, 2023.
- [4] W.-L. Chiang, Z. Li, Z. Lin, Y. Sheng, Z. Wu, H. Zhang, L. Zheng, S. Zhuang, Y. Zhuang, J. E. Gonzalez, I. Stoica, and E. P. Xing. Vicuna: An open-source chatbot impressing gpt-4 with 90%* chatgpt quality, March 2023. URL https://lmsys.org/blog/2023-03-30-vicuna/.
- [5] A. Deshpande, V. Murahari, T. Rajpurohit, A. Kalyan, and K. Narasimhan. Toxicity in chatgpt: Analyzing persona-assigned language models, 2023.
- [6] N. Liu, L. Chen, X. Tian, W. Zou, K. Chen, and M. Cui. From llm to conversational agent: A memory enhanced architecture with fine-tuning of large language models, 2024.
- [7] Y. Liu, G. Deng, Z. Xu, Y. Li, Y. Zheng, Y. Zhang, L. Zhao, T. Zhang, and Y. Liu. Jailbreaking chatgpt via prompt engineering: An empirical study, 2023.
- [8] OpenAI, :, J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman, D. Almeida, J. Altenschmidt, S. Altman, S. Anadkat, R. Avila, I. Babuschkin, S. Balaji, V. Balcom, P. Baltescu, H. Bao, M. Bavarian,

J.

Belgum,

I.

Bello,

J.

Berdine,

G.

Bernadett-Shapiro,

C.

Berner,

L.

Bogdonoff,

O.

Boiko,

M. Boyd,

A.-L.

Brakman,

G.

Brockman,

T.

Brooks,

M. Brundage, K. Button,

T.

Cai,

R.

Campbell,

A. Cann,

B. Carey, C. Carlson, R. Carmichael, B. Chan, C. Chang, F. Chantzis,

D. Chen, S. Chen, and R. C. et al.

Gpt-4 technical report, 2023.

- [9] L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. L. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray, J. Schulman, J. Hilton, F. Kelton, L. Miller, M. Simens, A. Askell, P. Welinder, P. Christiano, J. Leike, and R. Lowe. Training language models to follow instructions with human feedback, 2022.
- [10] D. shu, M. Jin, S. Zhu, B. Wang, Z. Zhou, C. Zhang, and Y. Zhang. Attackeval: How to evaluate the effectiveness of jailbreak attacking on large language models, 2024.
- [11] G. Team, R. Anil, S. Borgeaud, Y. Wu, J.-B. Alayrac, J. Yu, R. Soricut, J. Schalkwyk, A. M. Dai, A. Hauth, K. Millican, D. Silver, S. Petrov, M. Johnson, I. Antonoglou, J. Schrittwieser, A. Glaese, J. Chen, E. Pitler, T. Lillicrap, A. Lazaridou, O. Firat, J. Molloy, M. Isard, P. R. Barham, T. Hennigan, B. Lee, F. Viola, M. Reynolds, Y. Xu, R. Doherty, E. Collins, C. Meyer, E. Rutherford, E. Moreira, K. Ayoub, M. Goel, G. Tucker, E. Piqueras, M. Krikun, I. Barr, N. Savinov, I. Danihelka, B. Roelofs, A. White, A. Andreassen, T. von Glehn, L. Yagati, M. Kazemi, L. Gonzalez, M. Khalman, J. Sygnowski, A. Frechette, C. Smith, L. Culp, L. Proleev, Y. Luan, X. Chen, J. Lottes, N. Schucher, F. Lebron, A. Rrustemi, N. Clay, P. Crone, and T. K. et al. Gemini: A family of highly capable multimodal models, 2023.
- [12] H. Touvron, T. Lavril, G. Izacard, X. Martinet, M.-A. Lachaux, T. Lacroix, B. Rozi` ere, N. Goyal, E. Hambro, F. Azhar, A. Rodriguez, A. Joulin, E. Grave, and G. Lample. Llama: Open and efficient foundation language models, 2023.
- [13] H. Touvron, L. Martin, K. Stone, P. Albert, A. Almahairi, Y. Babaei, N. Bashlykov, S. Batra, P. Bhargava, S. Bhosale, D. Bikel, L. Blecher, C. C. Ferrer, M. Chen, G. Cucurull, D. Esiobu, J. Fernandes, J. Fu, W. Fu, B. Fuller, C. Gao, V. Goswami, N. Goyal, A. Hartshorn, S. Hosseini, R. Hou, H. Inan, M. Kardas, V. Kerkez, M. Khabsa, I. Kloumann, A. Korenev, P. S. Koura, M.-A. Lachaux, T. Lavril, J. Lee, D. Liskovich, Y. Lu, Y. Mao, X. Martinet, T. Mihaylov, P. Mishra, I. Molybog, Y. Nie, A. Poulton, J. Reizenstein, R. Rungta, K. Saladi, A. Schelten, R. Silva, E. M. Smith, R. Subramanian, X. E. Tan, B. Tang, R. Taylor, A. Williams, J. X. Kuan, P. Xu, Z. Yan, I. Zarov, Y. Zhang, A. Fan, M. Kambadur, S. Narang, A. Rodriguez, R. Stojnic, S. Edunov, and T. Scialom. Llama 2: Open foundation and fine-tuned chat models, 2023.
- [14] T. Vu, M. Iyyer, X. Wang, N. Constant, J. Wei, J. Wei, C. Tar, Y.H. Sung, D. Zhou, Q. Le, and T. Luong. Freshllms: Refreshing large language models with search engine augmentation, 2023.
- [15] A. Wei, N. Haghtalab, and J. Steinhardt. Jailbroken: How does llm safety training fail?, 2023.
- [16] Y. Zhu, H. Yuan, S. Wang, J. Liu, W. Liu, C. Deng, H. Chen, Z. Dou, and J.-R. Wen. Large language models for information retrieval: A survey, 2024.
- [17] A. Zou, Z. Wang, J. Z. Kolter, and M. Fredrikson. Universal and transferable adversarial attacks on aligned language models, 2023.