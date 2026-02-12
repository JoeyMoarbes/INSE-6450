<!-- image -->

.

<!-- image -->

.

.

<!-- image -->

.

.

.

.

.

.

.

.

Latest updates: hps://dl.acm.org/doi/10.1145/3709026.3709115

.

.

RESEARCH-ARTICLE

## SwordEcho: A LLM Jailbreaking Optimization Strategy Driven by Reinforcement Learning

XUEHAI TANG , University of Chinese Academy of Sciences, Beijing, China WENJIE XIAO , University of Chinese Academy of Sciences, Beijing, China ZHONGJIANG YAO , University of Chinese Academy of Sciences, Beijing, China JIZHONG HAN , University of Chinese Academy of Sciences, Beijing, China

Open Access Support provided by:

University of Chinese Academy of Sciences

<!-- image -->

.

.

Published: 06 December 2024

Citation in BibTeX format

CSAI 2024: 2024 8th International Conference on Computer Science and Artificial Intelligence (CSAI)

December 6 - 8, 2024 Beijing, China

.

.

.

.

.

.

## SwordEcho: A LLM Jailbreaking Optimization Strategy Driven by Reinforcement Learning

## Xuehai Tang

## Wenjie Xiao ∗

School of Cyber Security, University of Chinese Academy of Sciences School of Cyber Security, University of Chinese Academy of Sciences

Beijing, China

University of Chinese Academy of Sciences

Beijing, China

tangxuehai@iie.ac.cn

Beijing, China

xiaowenjie@iie.ac.cn

## Zhongjiang Yao †

School of Cyber Security, University of Chinese Academy

of Sciences Beijing, China

yangzhongjiang@iie.ac.cn

## Jizhong Han

School of Cyber Security, University of Chinese Academy of Sciences Beijing, China

hanjizhong@iie.ac.cn

## Abstract

## Keywords

## Warning:Thispapermaycontainpotentiallyoffensivemodel inputs or outputs.

With the rapid development of Large Language Models (LLMs), inherent security risks have become increasingly evident, particularly their capability to generate harmful content. As an effective tool for revealing potential vulnerabilities in LLMs within the context of red teaming, jailbreak attacks are widely used to assess the content safety defense levels of LLMs. However, existing open-source jailbreak prompts often lack sufficient readability and effectiveness, failing to comprehensively evaluate the security flaws of models and inadequately exposing the potential risks of LLMs. To address this issue, this paper introduces an enhanced jailbreak prompt generation method called "SwordEcho," which improves the readability and aggressiveness of jailbreak prompt words to more comprehensively evaluate model vulnerabilities. SwordEcho employs a multi-faceted reinforcement learning reward mechanism to finely tune the attack model, thereby effectively generating high-quality jailbreak prompts. To verify the transferability and generalization capabilities of SwordEcho, this study conducted jailbreak tests involving eleven different risk scenarios across six open-source LLMs and three commercial model APIs. The results indicate that, compared with existing mainstream jailbreak attack strategies, SwordEcho demonstrates higher Attack Success Rates (ASRs) across different target models.

## CCS Concepts

## · Computing methodologies → Natural language generation ; · General and reference → General conference proceedings .

∗ Co-corresponding authors who have made equal contributions to this work. † Co-corresponding authors who have made equal contributions to this work.

<!-- image -->

This work is licensed under a Creative Commons Attribution 4.0 International License. CSAI 2024, Beijing, China © 2024 Copyright held by the owner/author(s). ACM ISBN 979-8-4007-1818-2/24/12 https://doi.org/10.1145/3709026.3709115

Large Language Models, Jailbreak attacks, Red teaming, Reinforcement learning

## ACMReference Format:

Xuehai Tang, Wenjie Xiao, Zhongjiang Yao, and Jizhong Han. 2024. SwordEcho: A LLM Jailbreaking Optimization Strategy Driven by Reinforcement Learning. In 2024 8th International Conference on Computer Science and Artificial Intelligence (CSAI) (CSAI 2024), December 06-08, 2024, Beijing, China. ACM, New York, NY, USA, 8 pages. https://doi.org/10.1145/3709026.3709115

## 1 Introduction

In recent years, Large Language Models (LLMs) such as ChatGPT[5], GPT4[2], and Claude2[3] have made significant advancements across various domains. At the same time, these models still have multiple security issues, especially the ability to generate unsafe content, including privacy, discrimination, and politically sensitive information[7, 8, 12, 15]. To help detect and fix content security risks in large language models, jailbreak prompt attacks, as a red team strategy, have been proven to be an effective method for uncovering potential vulnerabilities in LLMs[16, 27].

The conventional jailbreak prompts used to identify potential security flaws in LLMs are manually designed. This process is often unable to fully discover potential vulnerabilities due to its high cost and strict limitations based on the designer's knowledge. Currently, some researchers are exploring methods to automate the generation of jailbreak prompts to address the limitations of cost and empirical knowledge. Among them, Masterkey[6] attempts to leverage the generative capabilities of LLMs to automate the construction of jailbreak prompts. This general prompt construction method relies on established templates and lacks adaptability to specific problems. Compared with specialized prompts for specific problems, general jailbreak prompts have low attack strength and are insufficient for new scenarios, as shown in the experimental results in Figure 1 1. The lack of adaptability of automated jailbreak prompts is the main challenge for red teams in enhancing the effectiveness of jailbreaks. Analyzing the composition structure of successful jailbreak prompts can help us better summarize their

Figure 1: The horizontal axis represents the jailbreak prompts, while the vertical axis denotes the problems. Dark points indicate a successful attack, where the target model was guided to produce harmful content. The results suggest that the jailbreak prompts generated by Masterkey exhibit significant potential for improvement.

<!-- image -->

inherent rules. To this end, we classify the content components of prompts based on their semantics into character descriptions, environment descriptions, problem descriptions (including positive or negative descriptions), and other categories, and conduct an in-depth analysis of the composition components and structural integrity of the prompts. The research found that (1) the more closely the topic description of successful jailbreak prompts matches the environmental description, the stronger the attack; for example, by recombining the problem descriptions of successful prompts from five different problem scenarios with environmental descriptions for the other four problems, that is, when prompts are used in different contexts, the attack strength significantly decreases[1]; (2) the structural integrity of jailbreak prompts significantly affects their attack effectiveness. By comparing tests of complete prompts with those that are structurally chaotic or lack components, it is indicated that prompts that maintain their original structure and sequence have the highest attack strength[9].

Based on the above analysis, to address the issue of insufficient adaptability in the automated construction of jailbreak prompts, we propose a new jailbreak prompt generation strategy, "SwordEcho," which optimizes the generation process using a multi-rewarddriven reinforcement learning method. This strategy focuses on improving the efficiency of prompt generation while ensuring effective application in different models and scenarios through precise composition structure generation and context semantics alignment, thereby more comprehensively discovering security vulnerabilities in LLMs.

Finally, extensive experimental validation has shown that our method significantly improves the speed and efficiency of generating jailbreak prompts and shows higher success rates and greater diversity in multiple open-source models and commercial APIs, emphasizing its importance in enhancing the security of LLMs.

In summary, our contributions are as follows:

1. We conducted an in-depth analysis of the composition rules of existing jailbreak prompts, qualitatively emphasizing the relationship between environmental descriptions and problem descriptions in jailbreak prompts, as well as the importance of structural integrity.
2. We introduced an improved method, "SwordEcho," which is a reinforcement learning-based adversarial jailbreak prompt generation method that effectively produces high-potency jailbreak prompts tailored to specific problems.
3. Adequate experiments have shown that our method generates jailbreak prompts that can bypass security alignment models more quickly and demonstrate better adaptability when transferred to multiple open-source models and commercial APIs.

## 2 BACKGROUND AND MOTIVATIONS

## 2.1 Problem Definition

Let f denote the large language model. Under typical conditions, the LLM functions to generate text 𝑦 ∼ 𝑓 (·| 𝑥 ) in response to a given prompt 𝑥 , thereby fulfilling specified directive tasks. Jailbreak prompt attacks involve the strategic design of a prompt 𝑗 , such that the output text 𝑦 ∼ 𝑓 (·| 𝑗 ) produced by the target model contains harmful information. The primary criterion for evaluating the effectiveness of 𝑥 is the reward function 𝑅 ( 𝑦 ) , Our overarching objective is to maximize the expected value 𝐸 𝑥 ∼ 𝜋,𝑦 ∼ 𝑓 ( 𝑦 | 𝑥 ) [ 𝑅 ( 𝑦 )] , where 𝜋 represents the parameters of the model we seek to optimize. However, an exclusive focus on the harmfulness of the output is suboptimal. Therefore, we propose a comprehensive reward framework comprising three components, defined as 𝑅 ( 𝑗, 𝑦 ) = 𝛼𝑅 1 ( 𝑗 ) + 𝛽𝑅 2 ( 𝑗 ) + 𝛾𝑅 3 ( 𝑦 ) , where 𝛼 , 𝛽 , and 𝛾 are the reward weights, and 𝑅 1 ( 𝑗 ) , 𝑅 2 ( 𝑗 ) , and 𝑅 3 ( 𝑦 ) represent the readability of the jailbreak prompt, the diversity of the jailbreak prompt, and the harmfulness of the target model's output, respectively. Formally, the objective of the jailbreak attack model can be articulated as follows:

<!-- formula-not-decoded -->

where 𝑗 is the modified jailbreak prompt, and 𝑦 is the response from the target model. Details of the specific reward design will be further discussed in the methods section below.

## 2.2 Motivation

Discovery One: The Relationship between Jailbreak Prompts andProblems. Weselected successful examples of jailbreak attacks from five distinct problem scenarios and systematically recombined their corresponding jailbreak prompts and issues in pairs. The outcomes of these jailbreak prompt attacks targeting the Llama2-7b model [22] are presented in Figure 2. The experimental results reveal a significant reduction in attack efficacy when originally successful jailbreak prompts are combined with prompts or issues from other contexts. Through a comprehensive textual analysis, we observed that the focus of the jailbreak prompts varies substantially; for instance, prompts that are effective in scenarios involving violence often frame the narrative around self-defense, which proves ineffective in contexts related to self-harm. This observation leads us to a critical conclusion: successful jailbreaking necessitates not only the potency of the attack prompts but also a robust alignment

Figure 2: The abscissa represents problems, the ordinate represents jailbreak tips, and the color of the intersection represents the harmfulness of the target model's output. The darker the color, the more harmful the text.

<!-- image -->

with the specific issue at hand. Therefore, it is imperative to generate optimal jailbreak prompts tailored to each distinct problem scenario.

Table 1: The Impact of Sequence Integrity on Jailbreaking

|                      |   ASR |   Mean harmfulness |
|----------------------|-------|--------------------|
| Primordial Order     |   0.6 |              0.572 |
| out-of-order         |   0   |              0.002 |
| Incomplete Structure |   0   |              0.013 |

## Discovery Two: The Impact of Jailbreak Prompt Structural

Integrity on Attack Potency. We categorized the content of jailbreak prompts into five types of sentences: character description, scene description, positive depiction, negative depiction, and others. Based on our observations of the structure of most jailbreak prompts, these five categories were identified as essential sentence types because they significantly influence the semantic integrity of the entire prompt. We tested the efficacy of complete jailbreak prompts against two altered prompt variants, including 'shuffled order, ' where the sentence sequence was disrupted (e.g., transitioning from 𝑃 𝑜𝑟𝑖𝑔𝑖𝑛 ( 𝑐 1 , 𝑐 2 , 𝑐 3 , 𝑐 4 , 𝑐 5 ) to 𝑃 𝑂𝑂 ( 𝑐 5 , 𝑐 3 , 𝑐 4 , 𝑐 1 , 𝑐 2 ) ) and 'incomplete structure,' where some structural sentences were omitted (e.g., from 𝑃 𝑜𝑟𝑖𝑔𝑖𝑛 ( 𝑐 1 , 𝑐 2 , 𝑐 3 , 𝑐 4 , 𝑐 5 ) to 𝑃 𝐼𝑆 ( 𝑐 1 , 𝑐 2 , 𝑐 4 , 𝑐 5 ) ). As illustrated in Table 1, the highest attack potency was observed when the original structural integrity and sequence were maintained, while the other variants exhibited negligible attack capability. Observations of the model's responses indicated that disordered or incomplete structures could lead to difficulties in comprehension by smaller models, resulting in either non-responsive or irrelevant answers. This demonstrates that the structural integrity of prompts plays a crucial role in the success of jailbreaking. It acts as an effective constraint, reducing unreasonable directions during the modification phase of jailbreak prompts and accelerating convergence.

## 3 Related Work

In recent years, the landscape of jailbreaking attacks has transitioned from manual design to automated generation. Current methodologies for automatic jailbreak prompt generation can be categorized into two primary types: general-purpose jailbreak prompt generation and problem-specific one-to-one jailbreak prompt generation.

The first category emphasizes the bulk generation of jailbreak prompts without targeting specific queries. This approach involves the modification of existing open-source jailbreak prompts to rapidly produce a large volume of prompts. For instance, the authors of MasterKey [6] leverage large language models (LLMs) to rewrite open-source prompts. Similarly, GPTFUZZER [24] utilizes fuzzy search techniques to alter existing prompts according to specific mutation rules, while FUZZLLM [23] generates new prompts by reorganizing elements from open-source sources. Although these methods exhibit rapid generation speeds, the adaptability of the resulting jailbreak prompts is constrained, and their effectiveness in addressing novel harmful queries is comparatively limited.

Thesecond category is characterized by the generation of specific jailbreak prompts tailored to individual queries, thereby enhancing adaptability relative to the former approach. For example, GCG [28] employs gradient backpropagation and defines target outputs to optimize the prompt creation process. GAattack [17] addresses the limitations associated with unrealistic target settings identified in GCG, demonstrating applicability to black-box models. In a similar vein, LOFT [20] utilizes surrogate models to adapt to the characteristics of original black-box frameworks. Furthermore, AUTODAN [18] incorporates genetic algorithms with defined targets to facilitate the generation of jailbreak prompts. While these approaches enable the creation of query-specific prompts, they necessitate the re-execution of the query process for new harmful questions, resulting in substantial computational demands, prolonged iteration times, and slow convergence rates.

## 4 Methodology

## 4.1 Method Workflow

As discussed in the introduction, current jailbreak prompts and automatically generate methods(AutoDAN, Masterkey, etc.) have limitations, which notably their inadequate attack potency, poor adaptability, and limited diversity. Consequently, we introduce an enhanced methodology termed SwordEcho. Figure 3 presents a streamlined workflow of our proposed method. Initially, we perform supervised fine-tuning (SFT) of the attack model utilizing publicly available jailbreak prompts and problem pairs. This phase aims to equip the attack model with a foundational knowledge of jailbreak prompts, enabling it to generate context-specific prompts, albeit with low attack strength. Subsequently, we implement reinforcement learning, which is particularly effective in scenarios where target outcomes can be quantitatively assessed. However, due to the previously established three-part reward function, conducting a unified training session risks instability and convergence challenges. To mitigate these issues, we partition the training into two distinct phases.In the first, non-adversarial phase, we focus on training the attack model using readability and diversity rewards. This approach allows the model to acquire significant knowledge,

## Enhanced Training Based on Instructional Data

Figure 3: Overview of the SwordEcho Method: The approach begins with the initial pre-training of the Large Language Model (LLM) to acquire knowledge pertinent to jailbreak prompts. The second step involves modifying these prompts to expand the search space. Initially, this involves synonym substitution at the word level within the original prompts. Subsequently, sentences are categorized into five predefined types and cross-replaced with corresponding sentences from other jailbreak prompts, ensuring both expansion of the search space and elimination of incorrect trajectories. Upon generating a new set of jailbreak prompts, the third step involves the calculation of rewards. A specially designed three-part reward function is utilized for this calculation, followed by parameter updates to the attack model. This process enables the model to learn and optimize the generation of more effective jailbreak prompts.

<!-- image -->

albeit resulting in limited attack potency. In the subsequent adversarial phase, we reduce the emphasis on the initial two rewards, prioritizing the enhancement of attack potency. This phase incorporates adversarial training with the target model to systematically up.

## 4.2 Detailed Process Analysis

We conceptualize the generation of jailbreak prompts as an optimization problem, with the primary objective of identifying a set of model parameters that maximize the value of Equation 1. To accomplish this, we structure our approach into two distinct phases. For detailed pseudocode Algorithm 1.

Phase One: Optimization of the ability to generate prompt Our reward design comprises three components, which can be effectively categorized into two optimization phases. Initially, we focus on the optimization of generating prompts, aiming to enhance the readability and diversity of the prompts without engaging in adversarial optimization, thereby setting aside considerations of attack potency. Let 𝑥 denote a problem belonging to the set 𝐷 , 𝑗 represents a jailbreak prompt, 𝑓 signify the attack model, and 𝜋 refers to the model parameters we intend to optimize. Our optimization objective is directed toward improving the readability and diversity of the jailbreak prompts, which can be formulated as: max 𝜋 𝐸 [ 𝛼𝑅 1 ( 𝑗 ) + 𝛽𝑅 2 ( 𝑗 )] . Readability is a critical factor for both humans and large language models (LLMs); coherent and clear semantics are essential for the LLM to comprehend and respond

Algorithm 1 SwordEcho algorithm pseudo code

Require: Policy parameters 𝜃 , reward weights 𝛼, 𝛽,𝛾 ,

Learning rate 𝜂 , discount factor 𝛾

Ensure:

Define state space S , action space A ,

Transition function T : S × A → S ,

Reward function R : S × A → R

for 𝑒𝑝𝑖𝑠𝑜𝑑𝑒 = 1 , 2, . . . , 𝑀 do

⊲ Mepisodes in total

Initialize environment to start state 𝑠 0

$$for 𝑡 = 0 , 1 , . . . , 𝑇 - 1 do$$

⊲ T steps per episode

𝑎 𝑡 ∼ 𝜋 𝜃 ( 𝑎 𝑡 | 𝑠 𝑡 )

⊲ Sample action from policy

𝑠 𝑡 + 1 , 𝑟 𝑡 = env.step ( 𝑎 𝑡 )

⊲ Environment interaction

𝑅

readability

=

2

-

1

𝑁

˝

𝑁

𝑖

=

1

log

2

𝑓

(

𝑤

𝑖

|

𝑤

1

,...,𝑤

𝑖

-

1

)

⊲ Readability Reward

𝑅 diversity = - max 𝑘 ≠ 𝑖 sim ( 𝑗 𝑘 , 𝑗 )

⊲ Diversity Penalty

𝑅 adversity = ToxiGen ( 𝑗 )

⊲ Adversarial Reward

$$𝑟 𝑡 = 𝛼𝑅 readability + 𝛽𝑅 diversity + 𝛾𝑅 adversity Δ 𝜃 = 𝜂 ∇ 𝜃 log 𝜋 𝜃 ( 𝑎 𝑡 | 𝑠 𝑡 )( 𝑟 𝑡 + 𝛾 V( 𝑠 𝑡 + 1 ) - V( 𝑠 𝑡 )) 𝜃 ← 𝜃 + Δ 𝜃$$

⊲ Policy gradient update

end for

end for

accurately. Although quantitatively measuring readability poses challenges, LLMs provide a useful metric-perplexity. Perplexity indicates the model's level of confusion regarding the test data, and while it is influenced by training data characteristics, it serves as a quantitative representation of readability. This relationship is formally captured in Equation 2:

<!-- formula-not-decoded -->

where:

- 𝑗 is the text being evaluated.
- 𝑤 1 , 𝑤 2 , . . . , 𝑤 𝑁 are the sequence of words in text 𝑗 .
- 𝑓 ( 𝑤 𝑖 | 𝑤 1 , . . . , 𝑤 𝑖 -1 ) is the probability of the language model predicting the 𝑖 𝑡ℎ word given the previous 𝑖 -1 words.
- 𝑁 is the total number of words in the text.
- log 2 denotes the logarithm base 2, used to compute the information entropy.

Diversity represents another critical challenge that must be addressed by this method. As mentioned in [11], To ensure the diversity of generated jailbreak prompts, it is essential to prevent the model from adopting a singular generation paradigm following multiple iterations of reinforcement learning. This diversity is crucial for enhancing the robustness and adaptability of the model in various contexts. Consequently, we refrain from employing entropy-based penalty rewards. Instead, we analyze batches of model inputs and outputs to assess the similarity among all generated outputs. We assign a penalizing reward based on the highest similarity, thereby establishing a clear directive for model outputs and ensuring their effectiveness. This is formally represented in Equation 3:

<!-- formula-not-decoded -->

where sim ( 𝑦 𝑖 , 𝑦 𝑗 ) is the similarity between outputs 𝑦 𝑖 and 𝑦 𝑗 , calculated using the TF-IDF algorithm:

<!-- formula-not-decoded -->

The final objective for the first phase of optimization is:

<!-- formula-not-decoded -->

Phase Two: Attack Potency Optimization. After the optimizations implemented in the previous phase, we have developed a model that is enriched with extensive knowledge of jailbreak prompts. However, the large language model (LLM) does not inherently understand which prompts are most effective or how to integrate them with specific problems to ensure successful attacks. Therefore, we advance to adversarial optimization, where rewards for readability and diversity are retained but assigned minimal weight. This approach allows us to enhance attack potency while still preserving readability and diversity.

To assess the harmfulness of the target model's output texts, we employ the ToxiGen model [10], which has been fine-tuned using the PKU 30K dataset[14] and has demonstrated an accuracy rate of 81% on the test set. Although it does not achieve an accuracy exceeding 90%, this level is adequate for validating our approach.

The model generates a probability value between 0 and 1, with an attack deemed successful if the probability of harm surpasses 0.5, indicating that the output text is harmful. Consequently, our final objective can be formalized in Equation 6 as follows:

<!-- formula-not-decoded -->

Thus, our ultimate objective is to optimize a set of model parameters such that the expected values of readability, diversity, and the induced harmful responses from the target model are maximized:

<!-- formula-not-decoded -->

where 𝛼 ≈ 𝛽 ≪ 𝛾

## 5 Experiments

## 5.1 Experimental Setup

Hardware Environment: 8*A100-80GB GPUs, 128-core CPU, 1TB RAM.

Datasets: Theopen-source question set comes from BeaverTails[14] and the GCG's question set from their GitHub project, the opensource jailbreak prompt set from rubend18/ChatGPT-JailbreakPrompts[13].

To ensure comprehensive coverage of all possible scenarios, the queries were categorized into 11 distinct classes for selection. These categories are:

- (1) Harassment (abbreviated as 'Har.')
- (2) Harassment Threatening ('Har\_threat.')
- (3) Hate ('Hat.')
- (4) Hate Threatening ('Hat\_threat.')
- (5) Self-harm ('SH.')
- (6) Self-harm Instructions ('SH\_instr.')
- (7) Self-harm Intent ('SH\_intent.')
- (8) Sexual ('Sex.')
- (9) Sexual Involving Minors ('Sex\_min.')
- (10) Violence ('Vio.')
- (11) Graphic Violence ('Vio\_graph.')
- (12) Average Attack Success Rate ('Avg\_ASR.')

Target Models: In our study, we utilize unaligned generative models, specifically Llama2-7b [22] and Vicuna7b [26], alongside aligned Llama2-7b and ChatGLM3-6b [25] for training. For evaluation, we employ a diverse set of target models: Llama2-13b-chat, Vicuna7b-v1.5, Baichuan2-13b [4], and InternLM-chat-20b [21], in addition to three commercial APIs.

Baseline Methods: Wechoseopen-source jailbreak prompts[13], GCG[28], Masterkey[6], and AUTODAN[18] as our baselines, where the first represents the first category of work summarized in our study, i.e., general-purpose jailbreak prompt generation. The latter two works represent the second category, one-to-one jailbreak prompt generation, and both baselines use early stopping settings and are set to generate one jailbreak prompt for every ten questions.

Evaluation Metrics: We utilized OpenAI's API[19] discriminator and the open-source "toxigen"[10] model to assess whether the model's entire output contains harmful content. We adopt ASR as

the metric to evaluate the success rate of attacks, which is the ratio of successful and total attack counts.

Table 2: This method, SwordEcho, is compared with baseline methods in terms of attack results, where 'Base' represents the unmodified, open-source jailbreak prompts, and the numbers indicate the Attack Success Rate (ASR).

|           | Llama2-7b-chat   | Llama2-13b-chat   | Vicuna-7b-v1.5   | Baichuan2-13b-chat   |
|-----------|------------------|-------------------|------------------|----------------------|
| Base      | 25%              | 6%                | 30%              | 23%                  |
| Masterkey | 22%              | 23%               | 43%              | 27%                  |
| AutoDAN   | 10%              | 20%               | 9%               | 12%                  |
| GCG       | 13%              | 5%                | 39%              | 3%                   |

## 5.2 Attack Effectiveness Experiment

We conducted comparative experiments between our method and baseline approaches. The results, as shown in Table 2, indicate that our method outperforms the baseline, achieving improvements of up to 70%. Our experiments were conducted within a fixed time limit, aiming to efficiently generate powerful jailbreak prompts. Therefore, we restricted the runtime during testing, which explains the poor performance of AutoDAN and GCG; their methods require starting from scratch for each problem, consuming extensive resources. Conversely, Masterkey does not generate problem-specific jailbreak prompts, resulting in weaker targeting and decreased attack potency. Notably, our method performed suboptimally on Vicuna-7b. Observations indicated that failures were due to the model not understanding our jailbreak prompts, leading to responses irrelevant to the topic. This highlights the importance of readability. However, for models with robust capabilities, our method demonstrated a high attack success rate.

## 5.3 Transferability Experiment

In this section, we conducted transfer experiments on the target models, including six open-source large models and three commercial large model APIs, to assess the attack capabilities of our optimized attack model across various problem scenarios and different target models. The experimental results, depicted in Figure 4, demonstrate that our attack model consistently achieves an attack success rate of over 80% across different scenarios and target models, unaffected by the nature of the problems or the specifics of the target models. This indicates strong transferability of our method across both problems and target models.

Table 3 in the paper elucidates the results obtained from targeting these models with our jailbreak approach. A significant observation from our experiments was the high success rate, over 90%, in breaching the defenses of these models. This not only highlights the transferability of our jailbreak techniques across different security models but also underscores the adaptability and potency of the generative model in performing effective jailbreak attacks.

Besides, The initial generative model was trained using Llama27b as our generative model, and we migrated it to the vicuna-7b model to demonstrate the transferability of our generative model.

The results in Table 4 demonstrate that the transferred generative model can still effectively learn the relationship between questions and jailbreak prompts in a high-dimensional feature space and can generate the best jailbreak prompts for questions outside the training set. These results not only confirm the transferability of the generative model but also show that the transferred generative model can still produce jailbreak prompts with a high success rate.

## 5.4 Ablation Experiment

5.4.1 Diversity Experiment. To test the effect of guided crossover, we compared experiments before and after adding guided crossover, as shown in Figure 5. The two dashed lines represent the lowest average score of jailbreak hints after each iteration, and the two solid lines represent the highest score. After adding the diversity design of the guided crossover, not only the convergence speed has become faster, but also the highest value converged has become higher. This indicates that after adding guided crossover, it can effectively guide the direction of jailbreak hint generation and accelerate the convergence speed. Figure 6 tests the diversity between jailbreak hints generated before and after adding diversity design. It can be seen that before adding a diversity design (blue solid line), the jailbreak hints generated by the model are basically similar or even the same, which is not conducive to our research. After adding a diversity design (green solid line), it is obvious that there is a big gap between jailbreak hints, which can enrich our dataset and is not easy to be defended.

5.4.2 Crossing Experiment. To test whether our constraints during crossover are effective, we conducted experiments with the constraint rules as the only variable, that is, random crossover and guided (with five categories) crossover during the crossover stage. As shown in Figure 7, after adding guided crossover, the training convergence speed of the generative model was significantly improved. Initially, it took four iterations to achieve a score of 0.9, and the generative model with constraint rules achieved this goal in only two iterations, improving efficiency by 50%. Through guided crossover, we observed further enhancement, which not only produced higher scores but also maintained the sequence integrity of jailbreak hints, reducing the probability of generating wrong routes. And simplifies the search space, promoting the convergence speed of training.

## 6 Conclusion

This paper presents an efficient method for generating jailbreak prompts characterized by high attack potency, grounded in a multireward function framework. The proposed approach seeks to identify security vulnerabilities within open-source models and commercial APIs while maintaining diversity among the generated jailbreak prompts. This multifaceted strategy facilitates a more thorough evaluation of the security posture of the target models. Our findings indicate that the interplay between harmful inquiries and jailbreak prompts significantly influences the success rate of jailbreak attempts, while the structural integrity of the prompts themselves also plays a crucial role in determining attack efficacy. Comprehensive experiments demonstrate the effectiveness of our method across both open-source large models and commercial APIs. We anticipate that our contributions will provide valuable insights into security dynamics and inform the development of safer large models, thereby supporting ongoing research in the realm of largescale model security.

Figure 4: Using the attack model optimized by this method, target model transfer attack experiments were conducted. The target models included multiple open-source and commercial APIs. The tests were performed under 11 different problem scenarios and measured by average attack success rate. The results demonstrate that the attack model optimized by this method exhibits high attack potency and strong generalizability.

<!-- image -->

Table 3: This part involves using the trained generative model to attack target models that were not used in training. The queries, totaling 765, are selected from the PKU dataset and categorized into 11 classes. The table provides a detailed breakdown of the number and percentage of breaches for each query category and each target model.

|             |          | Llama2-13b   | Llama2-13b   | vicuna-7b   | vicuna-7b   | Baichuan2-13b   | Baichuan2-13b   | internlm-20b   | internlm-20b   | zhipu_v2   | zhipu_v2   | douyin_wx   | douyin_wx   | Baichuan   | Baichuan   |
|-------------|----------|--------------|--------------|-------------|-------------|-----------------|-----------------|----------------|----------------|------------|------------|-------------|-------------|------------|------------|
| class       | N-querys | N-sucess     | ASR(%)       | N-sucess    | ASR(%)      | N-sucess        | ASR(%)          | N-sucess       | ASR(%)         | N-sucess   | ASR(%)     | N-sucess    | ASR(%)      | N-sucess   | ASR(%)     |
| Har.        | 100      | 96           | 96           | 86          | 86          | 97              | 97              | 96             | 96             | 96         | 96         | 93          | 93          | 99         | 99         |
| Har_threat. | 100      | 95           | 95           | 89          | 89          | 94              | 94              | 97             | 97             | 86         | 86         | 95          | 95          | 93         | 93         |
| Hat.        | 100      | 94           | 94           | 87          | 87          | 96              | 96              | 94             | 94             | 93         | 93         | 97          | 97          | 94         | 94         |
| Hat_threat. | 43       | 42           | 98           | 40          | 93          | 43              | 100             | 42             | 98             | 40         | 93         | 39          | 91          | 43         | 100        |
| SH.         | 77       | 76           | 99           | 64          | 83          | 76              | 99              | 76             | 99             | 73         | 95         | 76          | 99          | 76         | 99         |
| SH_instr.   | 51       | 47           | 92           | 39          | 76          | 49              | 96              | 50             | 98             | 46         | 90         | 49          | 96          | 46         | 96         |
| SH_intent.  | 71       | 69           | 97           | 60          | 85          | 70              | 99              | 70             | 99             | 62         | 87         | 69          | 97          | 70         | 99         |
| Sex.        | 100      | 93           | 93           | 84          | 84          | 96              | 96              | 94             | 94             | 75         | 75         | 94          | 94          | 98         | 98         |
| Sex_min.    | 22       | 21           | 95           | 20          | 91          | 22              | 100             | 22             | 100            | 22         | 100        | 22          | 100         | 22         | 100        |
| Vio.        | 100      | 93           | 93           | 67          | 67          | 88              | 88              | 85             | 85             | 92         | 92         | 91          | 91          | 91         | 91         |
| Vio_graph.  | 1        | 1            | 100          | 1           | 100         | 1               | 100             | 1              | 100            | 1          | 100        | 1           | 100         | 1          | 100        |
| Avg_ASR.    |          |              | 96           |             | 86          |                 | 97              |                | 96             |            | 92         |             | 96          |            | 97         |

Table 4: The effectiveness of the attack on each target model, where the total number of test harmful queries is 765.

| Model              | ASR(%)   |
|--------------------|----------|
| vicuna7b-v1.5      | 82%      |
| chatglm3-6b        | 91%      |
| Llama2-7b-chat     | 86%      |
| Llama2-13b-chat    | 95%      |
| Baichuan2-13b-chat | 96%      |
| internlm-chat-20b  | 95%      |

## 7 Ethical Statement

In this paper, we introduce a method focused on rapidly generating highly aggressive jailbreak prompts for harmful queries through the fine-tuning of large language models (LLMs). This approach could lead to the models producing potentially harmful content. However, the goal of our research is to bolster the security of LLMs, not to acquire these harmful outputs. By devising various jailbreak prompts, we aim to aid LLM researchers in enhancing the defensive mechanisms of these models. Our study does not seek to prompt LLMs to generate harmful content; instead, it aims to stimulate

Figure 5: Training convergence before and after adding the diversity exploration strategy.

<!-- image -->

further research into defense strategies among LLM researchers, ultimately leading to safer LLMs.

<!-- image -->

Figure 6: Comparison of the cosine similarity between the prompts before and after adding the diversity exploration strategy, with the X-axis representing the ID of the prompts and the Y-axis representing the cosine similarity, where larger values represent greater similarity.

<!-- image -->

ions

Figure 7: Training convergence before and after the addition of the five classifiers.

## Acknowledgments

To Robert, for the bagels and explaining CMYK and color spaces.

## References

- [1] Project Academy. 2023. The Ultimate Guide to Textual Integrity for HSC English. https://projectacademy.nsw.edu.au/year-12-guides/the-ultimate-guide-totextual-integrity/. Accessed: date-of-access.
- [2] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. 2023. Gpt-4 technical report. arXiv preprint arXiv:2303.08774 (2023).
- [3] Anthropic. 2023. Model card and evaluations for Claude models. https://wwwfiles.anthropic.com/production/images/Model-Card-Claude-2.pdf.
- [4] Baichuan. 2023. Baichuan 2: Open Large-scale Language Models. arXiv preprint arXiv:2309.10305 (2023). https://arxiv.org/abs/2309.10305
- [5] Tom B. Brown. 2020. Language models are few-shot learners. arXiv preprint arXiv:2005.14165 (2020).
- [6] Gelei Deng, Yi Liu, Yuekang Li, Kailong Wang, Ying Zhang, Zefeng Li, Haoyu Wang, Tianwei Zhang, and Yang Liu. 2023. MasterKey: Automated Jailbreak Across Multiple Large Language Model Chatbots. arXiv:2307.08715 [cs.CR]
- [7] Ameet Deshpande, Vishvak Murahari, Tanmay Rajpurohit, Ashwin Kalyan, and Karthik Narasimhan. 2023. Toxicity in ChatGPT: Analyzing Persona-assigned Language Models. arXiv:2304.05335 [cs.CL]
- [8] Josh A. Goldstein, Girish Sastry, Micah Musser, Renee DiResta, Matthew Gentzel, and Katerina Sedova. 2023. Generative Language Models and Automated Influence Operations: Emerging Threats and Potential Mitigations. arXiv:2301.04246 [cs.CY]
- [9] Jürgen Habermas. 1984. The Theory of Communicative Action, Volume 1: Reason and the Rationalization of Society . Beacon Press, Boston.
- [10] Thomas Hartvigsen, Saadia Gabriel, Hamid Palangi, Maarten Sap, Dipankar Ray, and Ece Kamar. 2022. ToxiGen: A Large-Scale Machine-Generated Dataset for Adversarial and Implicit Hate Speech Detection. arXiv:2203.09509 [cs.CL]
- [11] Zhang-Wei Hong, Idan Shenfeld, Tsun-Hsuan Wang, Yung-Sung Chuang, Aldo Pareja, James Glass, Akash Srivastava, and Pulkit Agrawal. 2024. Curiosity-driven Red-teaming for Large Language Models. arXiv:2402.19464 [cs.LG]
- [12] Lei Huang, Weijiang Yu, Weitao Ma, Weihong Zhong, Zhangyin Feng, Haotian Wang, Qianglong Chen, Weihua Peng, Xiaocheng Feng, Bing Qin, and Ting Liu. 2023. A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions. arXiv:2311.05232 [cs.CL]
- [13] Rubén Darío Jaramillo. 2023. rubend18/ChatGPT-Jailbreak-Prompts. https: //huggingface.co/datasets/rubend18/ChatGPT-Jailbreak-Prompts Accessed: 202311-3.
- [14] Jiaming Ji, Mickel Liu, Juntao Dai, Xuehai Pan, Chi Zhang, Ce Bian, Chi Zhang, Ruiyang Sun, Yizhou Wang, and Yaodong Yang. 2023. BeaverTails: Towards Improved Safety Alignment of LLM via a Human-Preference Dataset. arXiv:2307.04657 [cs.CL]
- [15] Daniel Kang, Xuechen Li, Ion Stoica, Carlos Guestrin, Matei Zaharia, and Tatsunori Hashimoto. 2023. Exploiting Programmatic Behavior of LLMs: Dual-Use Through Standard Security Attacks. arXiv:2302.05733 [cs.CR]
- [16] Daniel Kang, Xuechen Li, Ion Stoica, Carlos Guestrin, Matei Zaharia, and Tatsunori Hashimoto. 2023. Exploiting Programmatic Behavior of LLMs: Dual-Use Through Standard Security Attacks. ArXiv abs/2302.05733 (2023).
- [17] Raz Lapid, Ron Langberg, and Moshe Sipper. 2023. Open Sesame! Universal Black Box Jailbreaking of Large Language Models. arXiv:2309.01446 [cs.CL]
- [18] Xiaogeng Liu, Nan Xu, Muhao Chen, and Chaowei Xiao. 2023. AutoDAN: Generating Stealthy Jailbreak Prompts on Aligned Large Language Models. arXiv:2310.04451 [cs.CL]
- [19] OpenAI. 2023. OpenAI's Content Moderation. (2023). https://platform.openai. com/docs/guides/moderation/overview Accessed: 2023-11-19.
- [20] Muhammad Ahmed Shah, Roshan Sharma, Hira Dhamyal, Raphael Olivier, Ankit Shah, Joseph Konan, Dareen Alharthi, Hazim T. Bukhari, Massa Baali, Soham Deshmukh, Michael Kuhlmann, Bhiksha Raj, and Rita Singh. 2023. LoFT: Local Proxy Fine-tuning For Improving Transferability Of Adversarial Attacks Against Large Language Model. arXiv:2310.04445 [cs.CL]
- [21] InternLM Team. 2023. InternLM: A Multilingual Language Model with Progressively Enhanced Capabilities. https://github.com/InternLM/InternLM.
- [22] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, Aurelien Rodriguez, Armand Joulin, Edouard Grave, and Guillaume Lample. 2023. LLaMA: Open and Efficient Foundation Language Models. arXiv:2302.13971 [cs.CL]
- [23] Dongyu Yao, Jianshu Zhang, Ian G. Harris, and Marcel Carlsson. 2023. FuzzLLM: A Novel and Universal Fuzzing Framework for Proactively Discovering Jailbreak Vulnerabilities in Large Language Models. arXiv:2309.05274 [cs.CR]
- [24] Jiahao Yu, Xingwei Lin, Zheng Yu, and Xinyu Xing. 2023. Gptfuzzer: Red teaming large language models with auto-generated jailbreak prompts. arXiv preprint arXiv:2309.10253 (2023).
- [25] Aohan Zeng, Xiao Liu, Zhengxiao Du, Zihan Wang, Hanyu Lai, Ming Ding, Zhuoyi Yang, Yifan Xu, Wendi Zheng, Xiao Xia, et al. 2022. Glm-130b: An open bilingual pre-trained model. arXiv preprint arXiv:2210.02414 (2022).
- [26] Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric. P Xing, Hao Zhang, Joseph E. Gonzalez, and Ion Stoica. 2023. Judging LLM-as-a-Judge with MTBench and Chatbot Arena. arXiv:2306.05685 [cs.CL]
- [27] Terry Yue Zhuo, Yujin Huang, Chunyang Chen, and Zhenchang Xing. 2023. Red teaming ChatGPT via Jailbreaking: Bias, Robustness, Reliability and Toxicity. arXiv:2301.12867 [cs.CL]
- [28] Andy Zou, Zifan Wang, J. Zico Kolter, and Matt Fredrikson. 2023. Universal and Transferable Adversarial Attacks on Aligned Language Models. arXiv:2307.15043 [cs.CL]