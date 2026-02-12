<!-- image -->

## JBShield: Defending Large Language Models from Jailbreak Attacks through Activated Concept Analysis and Manipulation ∗

Shenyi Zhang 1 , Yuchen Zhai 1 , Keyan Guo 2 , Hongxin Hu 2 , Shengnan Guo 1 , Zheng Fang 1 , Lingchen Zhao 1 , Chao Shen 3 , Cong Wang 4 , and Qian Wang 1† 1 Key Laboratory of Aerospace Information Security and Trusted Computing, Ministry of Education, School of Cyber Science and Engineering, Wuhan University, 2 University at Buffalo, 3 Xi'an Jiaotong University, 4 City University of Hong Kong

## Abstract

Despite the implementation of safety alignment strategies, large language models (LLMs) remain vulnerable to jailbreak attacks, which undermine these safety guardrails and pose significant security threats. Some defenses have been proposed to detect or mitigate jailbreaks, but they are unable to withstand the test of time due to an insufficient understanding of jailbreak mechanisms. In this work, we investigate the mechanisms behind jailbreaks based on the Linear Representation Hypothesis (LRH), which states that neural networks encode high-level concepts as subspaces in their hidden representations. We define the toxic semantics in harmful and jailbreak prompts as toxic concepts and describe the semantics in jailbreak prompts that manipulate LLMs to comply with unsafe requests as jailbreak concepts. Through concept extraction and analysis, we reveal that LLMs can recognize the toxic concepts in both harmful and jailbreak prompts. However, unlike harmful prompts, jailbreak prompts activate the jailbreak concepts and alter the LLM output from rejection to compliance. Building on our analysis, we propose a comprehensive jailbreak defense framework, JBSHIELD, consisting of two key components: jailbreak detection JBSHIELD-D and mitigation JBSHIELD-M. JBSHIELD-D identifies jailbreak prompts by determining whether the input activates both toxic and jailbreak concepts. When a jailbreak prompt is detected, JBSHIELDMadjusts the hidden representations of the target LLM by enhancing the toxic concept and weakening the jailbreak concept, ensuring LLMs produce safe content. Extensive experiments demonstrate the superior performance of JBSHIELD, achieving an average detection accuracy of 0.95 and reducing the average attack success rate of various jailbreak attacks to 2% from 61% across distinct LLMs.

## 1 Introduction

Large language models (LLMs) have attracted significant research interest due to their ability to process and generate

∗ This is the full version of the paper accepted by USENIX Security 2025. † Corresponding author.

human-like text [1,5,26,43]. To prevent misuse, various safety alignment strategies, such as AI feedback [8,30] and reinforcement learning from human feedback (RLHF) [14,37], have been developed [25, 45, 47]. These strategies embed safety guardrails in LLMs to identify harmful or toxic semantics of prompts [27,31], thereby autonomously refusing harmful inputs and avoiding generating unsafe content. While these alignment methods have improved LLM safety and are widely used in both open-source and closed-source models [9, 29], they remain vulnerable to jailbreak attacks [6,10]. Jailbreak attacks subtly modify harmful inputs to create prompts that bypass these safety guardrails, causing LLMs to produce unsafe outputs that would normally be blocked. This poses significant security threats to real-world applications of LLMs.

To address the risks posed by jailbreaks, some studies have been proposed to detect or mitigate these attacks by analyzing the input and output of LLMs [3, 19, 22, 23, 40, 48, 51]. A few approaches [21,50,52] have sought to design defensive methods by understanding the effects of jailbreak prompts on LLMs, such as through the analysis of hidden representations or token distributions. These defenses often focus on some surface-level patterns between jailbreak and benign prompts, without understanding why jailbreak prompts can manipulate model behavior. However, without a systematic understanding of the underlying mechanisms that allow jailbreak prompts to alter LLMs behavior, these defenses fall short of providing truly robust protection that withstands the test of time [10,60].

In this paper, we investigate why LLMs respond to jailbreak prompts while rejecting the original harmful inputs to understand the mechanisms behind jailbreak attacks. This understanding enables us to design more robust jailbreak detection and mitigation methods. We pose two important research questions:

RQ1. Can aligned LLMs recognize the toxic semantics in jailbreak prompts?

RQ2. How do jailbreaks change the outputs of LLMs from rejecting to complying?

Figure 1: Illustration of how JBSHIELD defends aligned LLMs against jailbreak attacks.

<!-- image -->

To address RQ1 , we analyze and compare how the target LLM interprets toxic semantics in both jailbreak and harmful prompts. Based on the Linear Representation Hypothesis (LRH) [18, 35, 36], we define the toxic semantics in jailbreak and harmful prompts as the differences between their hidden representations and those of benign prompts, which we term as the 'toxic concepts.' By probing hidden representations and applying unsupervised linear decomposition, we define two toxic subspaces for the toxic concepts in both harmful and jailbreak prompts. In the comparison of the two subspaces, our analysis reveals that LLMs can recognize the toxic concept in both harmful and jailbreak inputs.

To address RQ2 , we derive the semantics that affect model behavior, termed the 'jailbreak concept,' from the representation differences between jailbreak and harmful prompts. By analyzing these results, we observe that Jailbreak attacks manipulate model behavior by introducing the jailbreak concept to increase the tendency to comply with user requests.

Based on our findings, we propose JBSHIELD, a comprehensive framework for jailbreak defense that analyzes and manipulates toxic and jailbreak concepts in the representation space of LLMs. Our framework consists of a jailbreak detection component JBSHIELD-D and a jailbreak mitigation component JBSHIELD-M. JBSHIELD-D initially uses a small set of calibration data to identify anchor subspaces that represent the toxic and jailbreak concepts. For a test prompt, JBSHIELD-D compares its representations with the anchor representations of benign and harmful prompts to extract the test toxic and jailbreak concepts. The subspaces of these test concepts are compared with the predefined anchor toxic and jailbreak subspaces to evaluate their similarity. A high similarity indicates that the corresponding concept has been activated. If both toxic and jailbreak concepts are activated, the test input is flagged as a jailbreak prompt. For mitigation, JBSHIELD-M provides a dynamic defense that can produce targeted safe content rather than issuing a fixed refusal output, as is common in most existing approaches. Specifically, for a detected jailbreak prompt, JBSHIELD-M strengthens the toxic concept to further alert the model and weakens the activation of the detected jailbreak concept to prevent undue manipulation of model behavior. Through these careful manipulations of the concepts, JBSHIELD enables efficient and interpretable jailbreak detection and mitigation.

We conduct extensive experiments to evaluate the performance of JBSHIELD. Against various types of jailbreak attacks on five open-source LLMs, JBSHIELD-D achieves an average F1-Score of 0.94. Additionally, JBSHIELD-M reduces the average attack success rates (ASR) of jailbreak attacks to 2%, showing superior defense capabilities. Notably, our method requires only 30 jailbreak prompts for calibration to achieve this performance. These results demonstrate that JBSHIELD significantly enhances the robustness of LLMs against jailbreaks and has the ability to rapidly adapt to new jailbreak techniques.

Our main contributions are summarized as follows:

- We reveal that jailbreak inputs drive LLMs to comply with unsafe requests by activating the jailbreak concept. Additionally, LLMs are capable of recognizing harmful semantics within jailbreak prompts through the activated toxic concept.
- We propose JBSHIELD 1 , a novel jailbreak defense framework that can detect and mitigate jailbreak attacks. By identifying and manipulating the toxic and jailbreak concepts, JBSHIELD can effectively detect jailbreak attacks in a single forward pass and enable the model to generate targeted safe outputs autonomously.
- We conduct extensive experiments to evaluate the effectiveness of JBSHIELD across five distinct LLMs against nine jailbreak attacks. The results show that our method significantly outperforms state-of-the-art (SOTA) defenses. Specifically, JBSHIELD achieves an average F1Score of 0.94 in detection and reduces the average attack success rate (ASR) from 61% to 2%.

## 2 Background and Related Works

## 2.1 Jailbreak Attacks on LLMs

Jailbreak attacks are designed to create malicious inputs that prompt target LLMs to generate outputs that violate predefined safety or ethical guidelines. Carlini et al. [10] first suggested that improved NLP adversarial attacks could achieve jailbreaking on aligned LLMs and encouraged further research in this area. Since then, various jailbreak attack methods have emerged. We categorize these attacks into five principal types: manual-designed jailbreaks, optimization-based

1 Our code and datasets are available at https://github.com/NISPLab/ JBShield

Table 1: Summary of existing jailbreak attacks. · indicates that the method utilizes the corresponding resource or has the specified capability. Conversely, ◦ denotes that the method does not use the listed resource or lacks that capability.

| Categories         | Jailbreaks       | Extra Assist   | White-box Access   | Black-box Attack   | TargetLLM Queries   | Soft Prompt Generated   | Template Optimization   |
|--------------------|------------------|----------------|--------------------|--------------------|---------------------|-------------------------|-------------------------|
| Manually-designed  | IJP [41]         | Human          | ◦                  | •                  | ◦                   | ◦                       | •                       |
| Optimization-based | GCG [65] SAA [4] | ◦ ◦            | •                  | Transfer Transfer  | ∼ 2K ∼ 10k          | • •                     | ◦ ◦                     |
|                    |                  |                | Logprobs           |                    |                     |                         |                         |
| Template-based     | MasterKey [16]   | LLM            | ◦                  | •                  | ∼ 200               | ◦                       | •                       |
| Template-based     | LLM-Fuzzer [57]  | LLM            | ◦                  | •                  | ∼ 500               | ◦                       | •                       |
| Template-based     | AutoDAN [64]     | LLM            | Logprobs           | Transfer           | ∼ 200               | ◦                       | •                       |
| Template-based     | PAIR [12]        | LLM            | ◦                  | •                  | ∼ 20                | ◦                       | •                       |
| Template-based     | TAP [34]         | LLM            | ◦                  | •                  | ∼ 20                | ◦                       | •                       |
| Linguistics-based  | DrAttack [32]    | LLM            | ◦                  | •                  | ∼ 10                | ◦                       | ◦                       |
| Linguistics-based  | Puzzler [11]     | LLM            | ◦                  | •                  | ◦                   | ◦                       | ◦                       |
| Encoding-based     | Zulu [55]        | ◦              | ◦                  | •                  | ◦                   | ◦                       | ◦                       |
| Encoding-based     | Base64 [46]      | ◦              | ◦                  | •                  | ◦                   | ◦                       | ◦                       |

jailbreaks, template-based jailbreaks, linguistics-based jailbreaks, and encoding-based jailbreaks. Table 1 provides a comprehensive summary of these attacks.

and Tree of Attacks with Pruning (TAP) [34] employ an attacker LLM to target another LLM explicitly, and successfully attack target models with minimal queries.

Manually-designed Jailbreaks . Manual-designed jailbreaks refer to attack strategies in which the adversarial prompts are delicately crafted by humans. Unlike automated methods that rely on algorithmic generation, these attacks are conceived directly by individuals who have a nuanced understanding of the operational mechanics and vulnerabilities of LLMs. In this study, we focus on in-the-wild jailbreak prompts (IJP) [41,58], which are real-world examples observed in actual deployments and shared by users on social media platforms.

Optimization-based Jailbreaks . Optimization-based jailbreaks use automated algorithms that exploit the internal gradients of LLMs to craft malicious soft prompts. Inspired by AutoPrompt, Greedy Coordinate Gradient (GCG) [65] employs a greedy algorithm to modify input prompts by adding an adversarial suffix, prompting the LLM to start its response with 'Sure' Building on GCG, Simple Adaptive Attacks (SAA) [4] use hand-crafted prompt templates and a random search strategy to find effective adversarial suffixes.

Template-based Jailbreaks . Template-based attacks generate jailbreak prompts by optimizing sophisticated templates and embedding the original harmful requests within them. Such prompts can bypass the safety guardrails of LLMs, making the model more likely to execute prohibited user requests [54]. MasterKey [16] trains a jailbreak-oriented LLM on a dataset of jailbreak prompts to generate effective adversarial inputs. LLM-Fuzzer [57] begins with human-written templates as seeds and uses an LLM to mutate these templates into new jailbreak inputs. AutoDAN [64] applies a hierarchical genetic algorithm for fine-grained optimization of jailbreak prompts at the sentence and word levels, assisted by an LLM. Prompt Automatic Iterative Refinement (PAIR) [12]

Linguistics-based Jailbreaks . Linguistics-based jailbreaks, also known as indirect jailbreaks, conceal malicious intentions within seemingly benign inputs to bypass defensive guardrails in target LLMs. DrAttack [32] decomposes and reconstructs malicious prompts, embedding the intent within the reassembled context to evade detection. Puzzler [11] analyzes LLM defense strategies and provides implicit clues about the original malicious query to the target model.

Encoding-Based Jailbreaks . Encoding-based jailbreaks manipulate the encoding or transformation of inputs to bypass LLM security measures. Zulu [55] translates inputs into low-resource languages, exploiting the limited capabilities of LLMs in these languages. Base64 [46] encodes malicious inputs in Base64 format to obfuscate their true intent.

## 2.2 Defenses against Jailbreaks

As jailbreak attacks on LLMs become more and more powerful, developing robust defenses is crucial. We review existing defense methods 2 , categorizing them into two main types: jailbreak detection and jailbreak mitigation [52]. A summary of jailbreak defenses is provided in Table 10.

Jailbreak Detection . Jailbreak detection aims to identify malicious inputs attempting to bypass guardrails in LLMs. Gradient cuff [21] detects jailbreak prompts by using the gradient norm of the refusal loss, based on the observation that malicious inputs are sensitive to perturbations in their hidden states. Self-Examination (Self-Ex) [19] feeds the model output back to itself to assess whether the response is harm-

2 Some of these methods initially just focus on input toxicity, but can be naturally extended to address jailbreaks.

ful, leveraging its ability to scrutinize the outputs. SmoothLLM [40] introduces random noise to outputs and monitors variability in responses to detect jailbreak inputs, exploiting the sensitivity of adversarial samples to perturbations. PPL [3] flags inputs as malicious if they produce perplexity above a certain threshold. GradSafe [50] distinguishes harmful from benign inputs by identifying different gradient patterns triggered in the model. The Llama-guard series [22] consists of LLMs fine-tuned specifically for harmful content detection. However, these methods rely on external safeguards that terminate interactions and generate fixed safe outputs, rather than enabling LLMs to produce safe responses autonomously. Jailbreak Mitigation . The goal of jailbreak mitigation is to preserve the integrity, safety, and intended functionality of LLMs, even when facing attempts to bypass their constraints. Self-Reminder (Self-Re) [51] modifies system prompts to remind the model to produce responsible outputs, reinforcing alignment with ethical guidelines. Paraphrase (PR) [23] uses LLMs to rephrase user inputs, filtering out potential jailbreak attempts. In-Context Defense (ICD) [48] incorporates demonstrations rejecting harmful prompts into user inputs, leveraging in-context learning to enhance robustness. SafeDecoding (SD) [52] fine-tunes the decoding module to prioritize safe tokens, reducing the risk of harmful outputs. Layer-specific Editing (LED) [60] fine-tunes the key layers critical for safety in LLMs, enhancing their robustness against manipulative inputs. Directed Representation Optimization (DRO) [62] fine-tunes a prefix of the input to shift harmful input representations closer to benign ones, promoting safer outputs.

## 3 Activated Concept Analysis

## 3.1 Overview

We utilize concept analysis to address the two research questions, RQ1 and RQ2 outlined in Section 1, and interpret why aligned LLMs respond to jailbreak prompts while rejecting original harmful inputs. We first define the semantic differences between harmful or jailbreak prompts and benign ones as the toxic concept . Similarly, the differences between jailbreak and harmful prompts as the jailbreak concept , which represents how jailbreak prompts affect LLMs. Guided by the LRH, we design a Concept Extraction algorithm that defines these concepts as subspaces within the hidden representations of LLMs. The pseudocode for the algorithm can be found in Appendix A. The comparisons between the toxic concepts extracted from harmful and jailbreak prompts show that LLMs actually can recognize harmful semantics in jailbreak prompts, similar to those in harmful prompts. Analyzing the differences between jailbreak and harmful prompts reveals that jailbreak attacks shift LLM outputs from rejecting to complying with malicious requests by introducing the jailbreak concept. This concept can override the influence of the toxic concept, thereby altering the behavior of the LLM.

## 3.2 Concept Extraction

We design a concept extraction algorithm to define high-level concepts activated in an LLM as subspaces within its hidden representations. Specifically, we define the semantic differences between jailbreak or harmful inputs and benign inputs as two toxic subspaces, defining two toxic concepts. Similarly, the semantic differences between jailbreak and harmful prompts form a jailbreak subspace, defining the jailbreak concept. Following LRH, our approach focuses on analyzing the hidden representations in the transformer layers to extract these concepts. For a given input prompt x , the l -th transformer layer in an LLM is formulated as

<!-- formula-not-decoded -->

where H l ( · ) ∈ R m × d denotes the hidden representation output from the l -th layer, which is the focus of our analysis. m is the number of tokens in the input prompt, and d is the embedding size of the target LLM. The extraction process for the three concepts, i.e., the two toxic concepts and the jailbreak concept, follows a similar method, differing only in the choice of prompt categories. We illustrate the detailed process of concept extraction at layer l using the toxic concept between harmful and benign prompts as an example:

Counterfactual Pair Formation . The high-level concepts mainly convey abstract semantics that are challenging to formalize. Following Park et al. [38], we represent a concept using counterfactual pairs of prompts. Given N harmful prompts, denoted as X h = { x h i } N i = 1 , and N benign prompts, denoted as X b = { x b i } N i = 1 , pairs are formed by randomly selecting one prompt from each category, resulting in the set ( x h 1 , x b 1 ) , ( x h 2 , x b 2 ) , . . . , ( x h N , x b N ) . Each pair ( x h i , x b i ) consists of prompts from different categories, aligned to highlight the semantic differences between them. While ideal counterfactual pairs would vary only by a single concept to ensure minimal variance between paired samples, achieving this with real-world datasets consisting of diverse samples presents significant challenges. Therefore, we construct counterfactual pairs by randomly pairing prompts from the two categories. Experimental results in Section 5 demonstrate that such counterfactual pairs are sufficient to capture the specific semantic differences required for our analysis. Since prompts consist of discrete tokens, direct analysis is challenging [2,59]. To address this, we use sentence embeddings generated by the target LLM to convert discrete prompts into continuous vectors. When predicting the next token, the hidden representation of the last token in LLMs captures rich contextual information and overall semantics. Thus, we select the hidden representation of the last token in H l as the sentence embedding e l for the entire input. This approach allows us to transform each counterfactual pair ( x h i , x b i ) into a pair of vectors ( e l ( x h i ) , e l ( x b i )) .

Linear Decomposition . In this step, we utilize counterfactual pairs to derive the corresponding subspace through linear decomposition. To extract linear components that distinguish between harmful and benign inputs, we first prepare the difference matrix D toxic by calculating the element-wise difference between corresponding harmful and benign prompt embeddings, as illustrated below:

<!-- formula-not-decoded -->

This approach ensures that each row in D toxic represents the direct difference vector between paired prompts, enhancing the relevance of the extracted components to the toxic concept. We then apply Singular Value Decomposition (SVD) to D toxic , which is particularly effective for elucidating the intrinsic structure of non-square matrices. For this analysis, we use the truncated SVD with rank = 1, focusing on the most significant singular vector. The first column of the resulting matrix V , denoted as v , captures the principal differences between the representations of harmful and benign prompts, serving as the key indicator of the toxic concept. We treat v as the subspace representing the concept C toxic ( X h , X b ) .

Mapping to Tokens . This step interprets high-level abstract concepts, such as toxic or jailbreak concepts, by mapping the subspace vector v into human-readable tokens. Using the output embedding matrix W oe of the LLM, we compute a score for each token in the vocabulary V as follows:

<!-- formula-not-decoded -->

These scores indicate how strongly each token aligns with the concept represented by v . The topk tokens { t i } k i = 1 with the highest scores are identified as interpretable representations of the concept. For example, tokens like 'sure' or 'yes' often align with jailbreak concepts, reflecting their role in reinforcing user compliance, while tokens like 'toxic' or 'danger' align with harmful semantics.

The extraction of the toxic concept using jailbreak and benign samples, as well as the extraction of the jailbreak concept using jailbreak and harmful samples, follows a similar process to the one described above. The only adjustment required is to replace the prompts in the counterfactual pairs accordingly. The tokens obtained from the concept extraction algorithm at layer 24 of Mistral-7B [26] for the three concepts are shown in Table 2. More results can be found in Appendix A, while the complete results for all layers across the five LLMs will be provided in the artifacts.

## 3.3 RQ1: Recognition of Harmful Semantics

To address RQ1 , we compare how LLMs recognize harmful semantics in jailbreak prompts versus original harmful prompts by extracting and analyzing the toxic concepts from

Table 2: Results of concept extraction on layer24 of Mistral7B. We remove all unreadable Unicode characters, retaining only interpretable words. Words in bold highlight tokens that support our findings on toxic and jailbreak concepts.

| Concepts           | Source Prompts                                                | Associated Interpretable Tokens                                                                                                                                                                                                                                                                                                                                                       |
|--------------------|---------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Toxic Concepts     | Harmful IJP GCG SAA AutoDAN PAIR DrAttack Puzzler Zulu Base64 | caution , warning , disclaimer , ethical understood, received, Received, hell caution , warning , disclaimer , warn sure, Sure, sorry , assured character, persona, caution , disclaimer caution , warning , disclaimer , ethical caution , sorry , unfortunately , Sorry bekan, implement, pdata, erste translate, sorry , transl, Translation decode, base, received, unfortunately |
| Jailbreak Concepts | IJP GCG SAA AutoDAN PAIR DrAttack Puzzler Zulu Base64         | understood , Hello, received , interpreted CHANT, Subject , plaat, bekan sure , Sure , mystery, CHANT character , protagon , persona , imagined yes , sure , Sure , Subject sure , Sure , response, Response bekan, occas, CHANT, plaat CHANT, translate , IMIT, translated decode , interpretation, received, reception                                                              |

both. The analysis of related tokens reveals several findings. First, we observe that aligned LLMs can recognize harmful semantics and associate them with human-readable tokens. For instance, tokens associated with the toxic concept activated by harmful prompts include words such as 'caution' and 'warning' (see Table 2 and Appendix A). This indicates the ability of the model to identify potential threats and generate self-warnings to avoid producing toxic content. While previous studies [7, 33, 53, 63] have observed differences in the hidden representations of harmful and benign inputs, often referring to the vector from benign to harmful regions as the 'refusal direction,' they lack explanations for the significance or cause of these differences. By extracting and analyzing toxic concepts, our method reveals that inputs with harmful semantics activate specific subspaces within hidden representations, known as toxic concepts. This provides a linear explanation for the differences in internal representation between harmful and benign samples, showing that these activated toxic concepts trigger the safety guardrails of the model, leading to the rejection of harmful inputs.

Secondly, we find that aligned LLMs can recognize harmful semantics within jailbreak prompts through the activation of toxic concepts. The tokens extracted from various jailbreak prompts are similar to those from harmful prompts. This finding addresses RQ1 , demonstrating that even when optimized by jailbreak attacks, the toxic semantics in jailbreak prompts remain detectable by the aligned LLM. However, this raises a further question within RQ2 : If toxic concepts are recognized in both cases, why do LLMs reject harmful inputs but com-

(a) Jailbreak Detection: JBShield-D

<!-- image -->

(b) Jailbreak Mitigation: JBShield-M

Figure 2: An illustration of JBSHIELD. Our jailbreak defense framework consists of two parts: jailbreak detection JBSHIELD-D and jailbreak mitigation JBSHIELD-M.

ply with jailbreak prompts? Understanding this distinction is crucial for comprehending how jailbreaks shift LLM outputs from rejection to compliance.

defenses against evolving jailbreak strategies. Observations across other models, detailed in Appendix A, confirm the robustness of these insights.

## 3.4 RQ2: Influence of Jailbreaks Prompts

To address RQ2 , which investigates why jailbreak attacks can influence LLM behavior, we leverage our concept extraction algorithm (Section 3.2) to identify and analyze the jailbreak concept-representing the semantic differences between jailbreak and original harmful prompts. Unlike prior works that focus only on surface-level behavioral changes in LLMs, our study reveals that jailbreak prompts will not bypass toxic detection but introduce new semantic components, termed 'jailbreak concepts,' that actively manipulate the model's compliance behavior. For instance, in Mistral7B, jailbreak methods like IJP [41], GCG [65], SAA [4], PAIR [12], and DrAttack [32] optimize prompts to generate responses like 'Sure, here is. . . ,' which reinforce the model's tendency to comply with user instructions. These activated jailbreak concepts are reflected in tokens such as understood,' sure,' and yes' (see Table 2), highlighting a semantic shift toward affirmative and compliance-related behavior. Similarly, AutoDAN [64], which employs role-playing scenarios like "imagine yourself in the character's shoes," is associated with tokens such as character' and persona,' emphasizing an induced persona-driven narrative. Approaches like Zulu [55] and Base64 [46] correspond to tokens such as translate' and 'decode,' reflecting their technical manipulation strategies.

These findings go beyond merely stating that jailbreak prompts influence LLMs; they systematically decode how distinct jailbreak concepts override toxic warnings, compelling the LLMs to produce harmful outputs. Moreover, by associating these abstract concepts with interpretable tokens, our method provides actionable insights into the mechanisms driving jailbreak incidents. This advancement allows us to not only understand but also design effective

## 4 JBSHIELD

## 4.1 Overview

Based on our analysis of jailbreak attack mechanisms, we propose JBSHIELD, a novel defense framework that counters jailbreak attacks by detecting and manipulating toxic and jailbreak concepts. An overview of JBSHIELD is provided in Figure 2.

Our framework consists of two components: JBSHIELD-D for jailbreak detection and JBSHIELD-M for jailbreak mitigation. The detection component, JBSHIELD-D, assesses whether the input contains harmful semantics and if it exhibits tendencies toward jailbreaking by detecting the activation of toxic and jailbreak concepts. JBSHIELD-D begins by using our concept extraction algorithm to create a concept subspace that captures the semantic differences between the input and benign samples. This test subspace is compared with an anchor toxic subspace, derived from a small set of benign and harmful prompts from the calibration dataset, to evaluate similarity. If the similarity is high, the input is flagged as activating the toxic concept. Similarly, a comparison with an anchor jailbreak subspace is made to determine if the jailbreak concept is activated. If both concepts are detected, the input is flagged as a jailbreak prompt.

Once a jailbreak input is identified, JBSHIELD-M enhances the toxic concept to alert the LLM by adding the anchor vector corresponding to the toxic subspace, while simultaneously weakening the jailbreak concept by subtracting the anchor vector corresponding to the jailbreak subspace from the hidden representations.

Note that JBSHIELD operates solely during the forward pass of LLMs and requires only minimal calibration data.

JBSHIELD-D completes detection with a single forward pass, while JBSHIELD-M involves only a few straightforward linear operations. This design allows for highly efficient jailbreak defense with minimal impact on the usability of the target LLM.

## 4.2 Jailbreak Detection

Our jailbreak detection method JBSHIELD-D involves four main steps: critical layer selection, anchor vector calibration, toxic concept detection, and jailbreak concept detection.

First, since not all layers in an LLM contribute equally to recognizing toxic concepts or responding to prompts with harmful semantics [60, 61], our approach begins by identifying the specific layers that can most accurately reflect the toxic and jailbreak concepts. All subsequent operations are conducted on these selected layers. Next, we obtain the anchor representations used for detection, which include those of benign and harmful samples, as well as the anchor toxic and jailbreak concept subspaces. The subspaces detected from new inputs are then compared with these anchor subspaces using cosine similarity to determine whether the corresponding concepts are activated. Then, we use the anchor representations of benign and harmful samples to extract the subspaces of the two concepts activated by the input, detecting whether the input activates the toxic and jailbreak concepts, respectively. If the cosine similarity between the subspaces extracted from the input and the anchor toxic and jailbreak subspaces exceeds a certain threshold, the input is classified as containing both concepts and is thus flagged as a jailbreak prompt.

Critical Layer Selection . Assuming we have calibration datasets consisting of N benign, N harmful, and N various jailbreak samples. We denote these benign samples as X b c = { x b i } n i = 1 , harmful samples as X h c = { x h i } n i = 1 , and jailbreak samples as X j c = { x j i } n i = 1 . In this step, we aim to identify the layers l t and l j that are best suited for detecting toxic and jailbreak concepts, respectively. The step begins by evaluating the representational quality across all layers of the model for each concept. If a particular layer shows a large difference in the embeddings between prompts of two different categories, it indicates that this layer has a stronger ability to capture the semantic gap between these categories [44,60]. We consider the analysis of the embeddings from this layer can yield more accurate subspaces. For the toxic concept, the average of cosine similarities between the sentence embeddings of harmful and benign samples in each layer l is calculated by

<!-- formula-not-decoded -->

where e l ( x h i ) and e l ( x b i ) represent the sentence embeddings at layer l for the i -th harmful sample x h i and benign sample x b i , respectively. We select the layer with the minimum average cosine similarity for toxic concept detection as

<!-- formula-not-decoded -->

This layer exhibits the greatest disparity in embeddings between harmful and benign samples, helping us identify a more accurate subspace corresponding to the toxic concept. Similarly, for the jailbreak concept, the layer l j is selected based on a comparative analysis between jailbreak and harmful prompts, following a similar process. This ensures that each selected layer l t and l j is where the embeddings most significantly reflect the corresponding concepts.

Anchor Vector Calibration . In this step, we first compute the anchor representations e l t b and e l j h for benign and harmful prompts. We use average sentence embeddings of benign prompts at layers l t as e l t b , and that of harmful prompts at layers l j as e l j h , which is presented as

<!-- formula-not-decoded -->

These embeddings serve as anchor representations for benign and harmful inputs. To calibrate the anchor subspaces for the toxic and jailbreak concepts, we then apply the calibration data to the Concept Extraction described in Section 3.2, resulting in two anchor subspaces, v t and v j for toxic concept and jailbreak concept. These two subspaces are used to determine whether subsequent test input activates the toxic and jailbreak concepts.

Toxic Concept Detection . The step begins when an input x is received, and its sentence embedding e l t x is computed at the critical layer l t identified for toxic concept detection. First, we form a difference matrix D t by e l t x and the anchor benign prompt embedding e l t b , which can be presented as

<!-- formula-not-decoded -->

Following Section 3.2, we then perform SVD on D t and get the subspace v toxic x . The subspace v toxic x is then compared to the anchor toxic concept subspace v t , utilizing cosine similarity to quantify the distance as

<!-- formula-not-decoded -->

If the cosine similarity exceeds a predetermined threshold Tt , the input is flagged as potentially activating the toxic concept. The threshold Tt is calculated using the harmful and benign samples from the calibration dataset. We apply these harmful and benign samples to the toxic concept detection described above, obtaining two sets of cosine similarity values. Tt is the threshold that best distinguishes these two sets of similarities. Specifically, we use Youden's J statistic [56] based on ROC curve analysis on these two sets of data as Tt . This statistic determines the optimal cutoff value that maximizes the difference between the true positive rate (sensitivity) and the false positive rate (1-specificity).

Jailbreak Concept Detection . This step focuses on detecting whether inputs activate the jailbreak concept. Similar to the previous step, a difference matrix D t is constructed at layer l j to compare e l j x with the anchor harmful prompt embedding e l j h as

<!-- formula-not-decoded -->

SVD is then applied to D j , and we can obtain a new v jailbreak x . The cosine similarity between v jailbreak x and the anchor jailbreak concept subspace v j is calculated as

<!-- formula-not-decoded -->

Apredefined threshold Tj , calibrated using known jailbreaking and harmful inputs, is used to determine whether v jailbreak x significantly activates the jailbreak concept. The threshold Tj is determined by harmful and jailbreak prompts in the calibration dataset, through a process similar to Tt in the toxic concept detection. An input x is conclusively identified as a jailbreak prompt when it simultaneously activates both toxic and jailbreak concepts above their respective thresholds. The result for identifying if an input prompt x is a jailbreak prompt is given by

<!-- formula-not-decoded -->

If the toxic concept and the jailbreak concept are both detected, the value of R ( x ) is set to True, and x is flagged as a jailbreak prompt.

## 4.3 Jailbreak Mitigation

Jailbreak detection can only identify whether the current input is a malicious jailbreak prompt, but it does not enable the LLM to provide targeted responses. Therefore, our jailbreak defense framework also includes a jailbreak mitigation method JBSHIELD-M. JBSHIELD-M operates in two steps. The first step is enhancing the toxic concept, which increases the resistance of the target LLM to harmful influences. The second one is weakening the jailbreak concept, which reduces the impact of jailbreak attacks on the LLM. By proactively modifying the internal states of critical layers, JBSHIELD-M ensures that the model outputs adhere to ethical guidelines and resist malicious manipulation.

Enhancing the Toxic Concept . The first step in mitigation is reinforcing the awareness of the target LLM for the toxic concept when a jailbreak input is identified. This is achieved by modifying the hidden representations at the critical layer l t identified for toxic concept detection. The adjustment involves a linear superposition of the toxic concept vector v t onto the hidden states H l t at layer l t , which can be formalized as

<!-- formula-not-decoded -->

which effectively enhances the awareness of harmful semantics in the input. The scaling factor δ t is crucial as it determines the intensity of the adjustment. To calculate δ t , we utilize harmful and benign prompts from the calibration dataset and get sets of harmful { e ( x h ) } x h ∈ X h c and benign { e ( x b ) } x b ∈ X h c sentence embeddings. For each embedding in these sets, we project the embeddings onto the toxic concept vector v t and calculate the mean of these projections for each category as

<!-- formula-not-decoded -->

The projection mean difference, which captures the average difference in the activation level of the toxic concept between harmful and benign inputs, is used to determine δ t as follows

<!-- formula-not-decoded -->

Careful selection of the value for δ t ensures that the intensity of the introduced additional toxic concept remains within a reasonable range, without affecting the normal functionality of the target LLM.

Weakening the Jailbreak Concept . Similar to the enhancement of the toxic concept, the adjustment in this step takes place at the critical layer l j identified for jailbreak concept detection. The hidden state H l j at this layer is modified by subtracting a scaled vector that represents the jailbreak concept

<!-- formula-not-decoded -->

where v j is the vector representing the jailbreak concept, obtained through the Anchor Vector Calibration described in JBSHIELD-D. The calculation of δ j mirrors the process used for δ t but focuses on the context of the jailbreak concept

<!-- formula-not-decoded -->

This targeted weakening of the jailbreak concept ensures that even if a malicious prompt successfully bypasses external detection, its ability to manipulate model behavior is significantly reduced.

## 5 Experiments

## 5.1 Data Collection and Preparation

We collect a diverse dataset comprising three primary categories of inputs: benign, harmful, and jailbreak prompts. We source our benign prompts from the Alpaca dataset [42], which is known for its rich and diverse real-world scenarios. A total of 850 benign prompts are randomly selected to form the benign segment of our dataset. For harmful inputs, we merge 520 prompts from the AdvBench dataset [65] with 330 prompts from the Hex-PHI dataset [39]. The jailbreak prompts are generated by applying nine different jailbreak attacks on five different LLMs. Among these attacks, in-thewild jailbreak prompts are directly sourced from the dataset released by Shen et al. [41], while the remaining jailbreak

Table 3: Effectiveness of the size N of the calibration dataset on Mistral-7B.

| Calibration Dataset Size N   | Accuracy ↑ /F1-Score ↑   | Accuracy ↑ /F1-Score ↑   | Accuracy ↑ /F1-Score ↑   | Accuracy ↑ /F1-Score ↑   | Accuracy ↑ /F1-Score ↑   | Accuracy ↑ /F1-Score ↑   | Accuracy ↑ /F1-Score ↑   | Accuracy ↑ /F1-Score ↑   | Accuracy ↑ /F1-Score ↑   |
|------------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|
| Calibration Dataset Size N   | IJP                      | GCG                      | SAA                      | AutoDAN                  | PAIR                     | DrAttack                 | Puzzler                  | Zulu                     | Base64                   |
| 10                           | 0.90/0.90                | 0.91/0.90                | 0.99/0.99                | 0.96/0.95                | 0.55/0.18                | 0.87/0.85                | 1.00/1.00                | 0.99/0.99                | 0.99/0.99                |
| 20                           | 0.88/0.89                | 0.95/0.95                | 0.99/0.99                | 0.97/0.97                | 0.80/0.84                | 0.87/0.85                | 1.00/1.00                | 0.99/0.99                | 0.99/0.99                |
| 30                           | 0.84/0.86                | 0.97/0.97                | 0.99/0.99                | 0.97/0.97                | 0.84/0.86                | 0.82/0.80                | 1.00/1.00                | 0.99/0.99                | 0.99/0.99                |
| 40                           | 0.85/0.87                | 0.96/0.97                | 0.99/0.99                | 0.96/0.97                | 0.81/0.82                | 0.82/0.80                | 1.00/1.00                | 0.99/0.99                | 0.99/0.99                |
| 50                           | 0.81/0.84                | 0.96/0.96                | 0.99/0.99                | 0.96/0.96                | 0.79/0.80                | 0.78/0.77                | 0.99/0.66                | 0.99/0.99                | 0.99/0.99                |

prompts are specifically generated to target the harmful samples in our dataset. We use the default settings for all the attacks when generating these jailbreak samples, resulting in a total of 32,600 jailbreak prompts. In all experiments, we randomly select N harmful, benign, and jailbreak prompts from our dataset to form the calibration dataset, with the remaining prompts used as the test set. The calibration dataset is used to calibrate the anchor vectors in JBSHIELD. All subsequent experimental results are obtained on the test set. A more detailed description and summary of our dataset can be found in Appendix B.1.

SD and DRO require modifications to the model, involving fine-tuning processes, whereas the other methods do not necessitate changes to the protected LLM. A detailed introduction to the implementations of each method can be found in Appendix B.4.

## 5.2 Experimental Setup

Models . In our experiments, we utilized a selection of five open-source LLMs, namely Mistral-7B (Mistral-7B-Instructv0.2) [26], Vicuna-7B (vicuna-7b-v1.5), Vicuna-13B (vicuna13b-v1.5) [13], Llama2-7B (Llama-2-7b-chat-hf) [43] and Llama3-8B (Meta-Llama-3-8B-Instruct) [17] from three different model families. These models encompass various model sizes, training data, and alignment processes, providing a comprehensive insight into the existing range of models.

Attack Methods . We evaluate the performance of JBSHIELD in defending nine different jailbreak attacks on selected LLMs. These attacks fall into five different categories, including the manually-designed IJP [41], optimization-based jailbreaks GCG [65] and SAA [4], template-based attacks AutoDAN [64] and PAIR [12], linguistics-based attacks DrAttack [32] and Puzzler [11], and encoding-based attacks Zulu [55] and Base64 [46]. Details on the hyperparameters and deployment of these jailbreak attacks can be found in Appendix B.3.

Baselines . To evaluate the effectiveness of JBSHIELD, we compare it against 10 SOTA methods in the field as baselines. These baselines are grouped into two categories based on their primary objectives: jailbreak detection and jailbreak mitigation. For detection, we compare JBSHIELD with Perspective API (PAPI) [28], PPL [3], Llama Guard (LlamaG) [22], SelfEx [19], and GradSafe [50]. For mitigation, Self-Re [51], PR [23], ICD [48], SD [52], and DRO [62] are considered. Notably, some of the baselines, such as LlamaG and GradSafe, are primarily designed for toxic content detection and are not specifically tailored to address jailbreak scenarios.

Metrics . We use detection accuracy and F1-Score to evaluate the effectiveness of jailbreak detection methods, while the attack success rate (ASR) is used to assess the performance of the jailbreak mitigation method. Jailbreak detection accuracy reflects the ability of the defenses to identify jailbreak prompts. The F1-Score, which incorporates precision, provides insight into the false positive rate of detection methods-that is, whether benign inputs are mistakenly identified as jailbreak prompts. In experiments of jailbreak mitigation, we manually evaluate whether Zulu and Base64 successfully jailbreak the model. For other attacks, we use SORRY-Bench [49] to determine whether a jailbreak attack has successfully bypassed the defense method and caused the model to comply with the jailbreak input to generate unsafe content. The attack success rate is then calculated to reflect the performance of the defenses.

## 5.3 Hyperparameter Analysis

We conduct hyperparameter analysis to determine the size N of the calibration dataset used in JBSHIELD. We tested detection accuracy and F1-Score on Mistral-7B for different values of N (10, 20, 30, 40, and 50). The results are shown in Table 3. As observed, our method performs best in detecting GCG, AutoDAN, and PAIR when N is set to 30. For the remaining jailbreaks, JBSHIELD-D efficiently detects these attacks with N set to just 10. Notably, for IJP and DrAttack, increasing the number of calibration samples leads to overfitting. Based on the trade-off between detection effectiveness and data efficiency, we set N to 30 for all experiments.

## 5.4 Jailbreak Detection

In this experiment, we use a calibration dataset comprising 30 benign, 30 harmful, and 30 corresponding jailbreak prompts, totaling 90 samples, to obtain the anchor vectors for each jailbreak. We consistently select an equal number of test benign prompts and test jailbreak prompts to compute jailbreak

Table 4: Performance of different jailbreak detection methods.

| Methods    | Accuracy ↑ / F1-Score ↑   | Accuracy ↑ / F1-Score ↑   | Accuracy ↑ / F1-Score ↑   | Accuracy ↑ / F1-Score ↑   | Accuracy ↑ / F1-Score ↑   | Accuracy ↑ / F1-Score ↑   | Accuracy ↑ / F1-Score ↑   | Accuracy ↑ / F1-Score ↑   | Accuracy ↑ / F1-Score ↑   |
|------------|---------------------------|---------------------------|---------------------------|---------------------------|---------------------------|---------------------------|---------------------------|---------------------------|---------------------------|
| Methods    | IJP                       | GCG                       | SAA                       | AutoDAN                   | PAIR                      | DrAttack                  | Puzzler                   | Zulu                      | Base64                    |
| Mistral-7B | Mistral-7B                | Mistral-7B                | Mistral-7B                | Mistral-7B                | Mistral-7B                | Mistral-7B                | Mistral-7B                | Mistral-7B                | Mistral-7B                |
| PAPI       | 0.04/0.08                 | 0.05/0.09                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 |
| PPL        | 0.01/0.03                 | 0.33/0.48                 | 0.00/0.00                 | 0.00/0.00                 | 0.01/0.01                 | 0.00/0.00                 | 0.00/0.00                 | 0.95/0.95                 | 0.00/0.00                 |
| LlamaG     | 0.68/0.81                 | 0.78/0.87                 | 0.83/0.90                 | 0.77/0.87                 | 0.74/0.85                 | 0.84/0.91                 | 0.77/0.87                 | 0.50/0.67                 | 0.58/0.73                 |
| Self-Ex    | 0.42/0.59                 | 0.52/0.68                 | 0.40/0.57                 | 0.56/0.72                 | 0.46/0.63                 | 0.51/0.67                 | 0.44/0.62                 | 0.32/0.49                 | 0.37/0.54                 |
| GradSafe   | 0.01/0.02                 | 0.63/0.77                 | 0.00/0.00                 | 0.00/0.00                 | 0.05/0.10                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 |
| Ours       | 0.84/0.86                 | 0.97/0.97                 | 0.99/0.99                 | 0.97/0.97                 | 0.84/0.86                 | 0.82/0.80                 | 1.00/1.00                 | 0.99/0.99                 | 0.99/0.99                 |
| Vicuna-7B  | Vicuna-7B                 | Vicuna-7B                 | Vicuna-7B                 | Vicuna-7B                 | Vicuna-7B                 | Vicuna-7B                 | Vicuna-7B                 | Vicuna-7B                 | Vicuna-7B                 |
| PAPI       | 0.04/0.08                 | 0.14/0.25                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 |
| PPL        | 0.01/0.03                 | 0.47/0.62                 | 0.00/0.00                 | 0.01/0.02                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.95/0.95                 | 0.00/0.00                 |
| LlamaG     | 0.65/0.79                 | 0.75/0.86                 | 0.85/0.91                 | 0.72/0.83                 | 0.75/0.85                 | 0.84/0.91                 | 0.75/0.86                 | 0.49/0.65                 | 0.55/0.71                 |
| Self-Ex    | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.01/0.02                 | 0.01/0.03                 |
| GradSafe   | 0.03/0.06                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.03/0.06                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 |
| Ours       | 0.82/0.83                 | 0.95/0.96                 | 0.99/0.99                 | 0.97/0.97                 | 0.91/0.91                 | 0.99/0.99                 | 1.00/0.91                 | 0.99/0.99                 | 1.00/1.00                 |
| Vicuna-13B | Vicuna-13B                | Vicuna-13B                | Vicuna-13B                | Vicuna-13B                | Vicuna-13B                | Vicuna-13B                | Vicuna-13B                | Vicuna-13B                | Vicuna-13B                |
| PAPI       | 0.04/0.08                 | 0.02/0.04                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 |
| PPL        | 0.01/0.03                 | 0.79/0.86                 | 0.00/0.00                 | 0.01/0.02                 | 0.01/0.02                 | 0.00/0.00                 | 0.00/0.00                 | 0.95/0.95                 | 0.00/0.00                 |
| LlamaG     | 0.64/0.77                 | 0.76/0.86                 | 0.84/0.91                 | 0.75/0.76                 | 0.76/0.86                 | 0.85/0.92                 | 0.75/0.85                 | 0.48/0.64                 | 0.54/0.70                 |
| Self-Ex    | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 |
| GradSafe   | 0.01/0.02                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 |
| Ours       | 0.99/0.98                 | 0.99/0.99                 | 0.99/0.99                 | 0.99/0.99                 | 0.98/0.99                 | 0.95/0.98                 | 1.00/0.75                 | 0.99/0.99                 | 1.00/1.00                 |
| Llama2-7B  | Llama2-7B                 | Llama2-7B                 | Llama2-7B                 | Llama2-7B                 | Llama2-7B                 | Llama2-7B                 | Llama2-7B                 | Llama2-7B                 | Llama2-7B                 |
| PAPI       | 0.04/0.08                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 |
| PPL        | 0.01/0.03                 | 0.79/0.86                 | 0.00/0.00                 | 0.10/0.18                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.95/0.95                 | 0.00/0.00                 |
| LlamaG     | 0.41/0.57                 | 0.32/0.48                 | 0.63/0.77                 | 0.38/0.55                 | 0.53/0.69                 | 0.57/0.72                 | 0.49/0.65                 | 0.30/0.46                 | 0.35/0.51                 |
| Self-Ex    | 0.31/0.33                 | 0.28/0.32                 | 0.36/0.39                 | 0.27/0.31                 | 0.27/0.30                 | 0.32/0.35                 | 0.24/0.27                 | 0.30/0.33                 | 0.29/0.32                 |
| GradSafe   | 0.39/0.56                 | 0.97/0.98                 | 0.00/0.00                 | 0.96/0.98                 | 0.62/0.77                 | 0.00/0.00                 | 0.18/0.31                 | 0.00/0.00                 | 0.00/0.00                 |
| Ours       | 0.84/0.86                 | 0.82/0.86                 | 0.93/0.94                 | 0.98/0.98                 | 0.87/0.88                 | 0.99/0.99                 | 0.81/0.85                 | 0.91/0.91                 | 0.92/0.93                 |
| Llama3-8B  | Llama3-8B                 | Llama3-8B                 | Llama3-8B                 | Llama3-8B                 | Llama3-8B                 | Llama3-8B                 | Llama3-8B                 | Llama3-8B                 | Llama3-8B                 |
| PAPI       | 0.04/0.08                 | 0.02/0.04                 | 0.00/0.00                 | 0.02/0.04                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 |
| PPL        | 0.01/0.03                 | 0.85/0.90                 | 0.00/0.00                 | 0.23/0.36                 | 0.00/0.00                 | 0.00/0.00                 | 0.00/0.00                 | 0.95/0.95                 | 0.00/0.00                 |
| LlamaG     | 0.46/0.63                 | 0.54/0.70                 | 0.71/0.83                 | 0.50/0.67                 | 0.60/0.75                 | 0.70/0.82                 | 0.55/0.71                 | 0.34/0.51                 | 0.38/0.56                 |
| Self-Ex    | 0.15/0.26                 | 0.12/0.21                 | 0.19/0.31                 | 0.11/0.19                 | 0.16/0.26                 | 0.16/0.27                 | 0.18/0.30                 | 0.12/0.21                 | 0.14/0.24                 |
| GradSafe   | 0.41/0.58                 | 0.21/0.35                 | 0.00/0.00                 | 0.97/0.98                 | 0.37/0.54                 | 0.00/0.00                 | 0.92/0.96                 | 0.00/0.00                 | 0.00/0.00                 |
| Ours       | 0.91/0.92                 | 0.98/0.99                 | 1.00/1.00                 | 0.97/0.97                 | 0.77/0.86                 | 0.97/0.96                 | 0.99/0.99                 | 0.99/0.99                 | 0.97/0.97                 |

detection accuracy and F1-Score. This ensures that detection methods perform well in identifying jailbreak prompts and the false positive rate for benign samples is demonstrated.

Detection Performance . We compared the jailbreak detection performance of our JBSHIELD-D on five LLMs against nine different jailbreak attacks, as shown in Table 4. It can be observed that our method achieves superior detection accuracy and F1 scores, significantly outperforming existing methods. For nine jailbreaks across five LLMs, JBSHIELD-D achieves an average detection accuracy of 0.95 and an average F1-Score of 0.94. Among all the baselines, the PAPI almost fails to detect jailbreak prompts, and PPL is only effective against GCG, which has a high proportion of soft prompts. Due to the weaker contextual learning abilities of some LLMs, they may not understand the prompts used by Self-Ex, rendering this baseline almost ineffective on the Vicuna series LLMs. GradSafe performs relatively well only on the Llama series models. For example, it achieves an F1 score of 0.98 for GCG on Llama2-7B, but it is completely ineffective against SAA, DrAttack, Zulu, and Base64. LlamaG demonstrates the best overall performance among the baselines and even outperforms our method when facing DrAttack on Mistral7B. However, LlamaG requires a large amount of data to fine-tune a new LLM, and it does not maintain such high ef-

Figure 3: Transferability of JBSHIELD-D.

<!-- image -->

ficiency across all models or against all attacks. In all cases, LlamaG achieves an accuracy/F1-Score of 0.62/0.75, which is 38%/21% lower than our method. These results demonstrate the superior effectiveness of our method in detecting various jailbreaks across different LLMs.

Transferability . In order to investigate the transferability of JBSHIELD, we used jailbreak prompts from different attacks in the calibration dataset and the test set to evaluate the performance of JBSHIELD-D against unknown jailbreak attacks. In order to investigate the transferability of JBSHIELD, we use jailbreak prompts from different attacks in the calibration dataset and the test set to evaluate the performance of JBSHIELD-D against unknown jailbreak attacks. The transferability results on Mistral-7B are shown in Figure 3. In most cases, our method achieves an accuracy above 0.84 and an F1 score above 0.86. Notably, JBSHIELD-D achieves an accuracy and F1 score above 0.90 when detecting AutoDAN, Zulu, and Base64 samples, regardless of which jailbreak prompts were used for calibration. However, we also observe that JBSHIELD-D exhibited weaker transferability for Puzzler. While the accuracy remained around 0.75, the F1 score dropped to below 0.2. This could be due to the significant difference in the activation strength of its toxic concept compared to other jailbreaks, resulting in a higher false positive rate. Overall, our method demonstrates significant transferability across different jailbreak attacks. This indicates that our method possesses notable robustness even when facing unknown and different types of jailbreak attacks.

Evaluation on Non-model-specific Jailbreak Prompts . To evaluate the model-agnostic effectiveness of JBSHIELD-D, we conducted an experiment using 100 in-the-wild jailbreak prompts that successfully bypassed all five LLMs (as determined by SORRY-Bench). Among these, 30 prompts were randomly selected for calibration, while the remaining 70 were used for testing across the five LLMs. The results, presented in Table 5, demonstrate that JBSHIELD-D achieves robust detection performance even in a non-model-specific setting, maintaining high detection accuracy across all tested models. This validates the versatility and generalizability of our approach under practical scenarios.

Prompts with Only Jailbreak Concept . To further evaluate JBSHIELD-D, we conducted an experiment using 850 jail-

Table 5: Performance on non-model-specific jailbreaks.

| Models     |   Accuracy ↑ |   F1-Score ↑ |
|------------|--------------|--------------|
| Mistral-7B |         0.88 |         0.88 |
| Vicuna-7B  |         0.87 |         0.87 |
| Vicuna-13B |         0.79 |         0.78 |
| Llama2-7B  |         0.84 |         0.86 |
| Llama3-8B  |         0.86 |         0.87 |

Table 6: Performance on prompts with only jailbreak concept.

| Models     |   Toxic Detected ↓ |   Jailbreak Detected ↑ |   Accuracy ↑ |   F1-Score ↑ |
|------------|--------------------|------------------------|--------------|--------------|
| Mistral-7B |                692 |                    158 |         0.19 |         0.31 |
| Vicuna-7B  |                 79 |                    771 |         0.91 |         0.95 |
| Vicuna-13B |                686 |                    164 |         0.19 |         0.32 |
| Llama2-7B  |                 23 |                    827 |         0.97 |         0.99 |
| Llama3-8B  |                 57 |                    793 |         0.94 |         0.97 |

break prompts generated by AutoDAN, where the malicious content was replaced with benign content to simulate cases that activate the jailbreak concept without triggering toxic activation. These modified prompts were tested across five LLMs, and the results are summarized in Table 6. Our findings indicate that JBSHIELD-D performs exceptionally well on Llama and Vicuna-7B, accurately identifying such inputs as non-jailbreak. However, its performance slightly declined on Mistral-7B and Vicuna-13B. This indicates a potential limitation of our approach in handling nuanced cases where jailbreak activation subtly interacts with the model's semantic interpretations. Since our primary focus is on robust jailbreak defense, optimizing performance for these complex scenarios remains an avenue for future work.

## 5.5 Jailbreak Mitigation

We evaluate the performance of our method by comparing the reduction in ASR of JBSHIELD-M against five jailbreak mitigation baselines across nine selected jailbreak attacks. Among these attacks, IJP, Puzzler, Zulu, and Base64 are transfer-based attacks that do not directly exploit the information of the target LLM. For these jailbreaks, we randomly select 50 corresponding jailbreak prompts from our dataset to test and determine the ASR for each attack. For the other jailbreak methods, we treat the defended model as a new target LLM, generate 50 new jailbreak prompts, and calculate the ASR.

Mitigation Efficiency . The ASRs of nine jailbreak attacks on LLMs deployed with JBSHIELD-M and five baselines are shown in Table 7. Our method reduces the ASR of most jailbreak attacks to zero, significantly outperforming the baselines. Across all five LLMs, JBSHIELD-M lowers the average ASR from 61% to 2%. Notably, our method renders the ASR of AutoDAN, Puzzler, and Base64 attacks 0.00, effectively defending them. Among all the baselines, SD performs

Table 7: Performance of different jailbreak mitigation methods. No-Def means no defense is deployed.

| Methods   | Attack Success Rate ↓   | Attack Success Rate ↓   | Attack Success Rate ↓   | Attack Success Rate ↓   | Attack Success Rate ↓   | Attack Success Rate ↓   | Attack Success Rate ↓   | Attack Success Rate ↓   | Attack Success Rate ↓   | Average ASR ↓   |
|-----------|-------------------------|-------------------------|-------------------------|-------------------------|-------------------------|-------------------------|-------------------------|-------------------------|-------------------------|-----------------|
| Methods   | IJP                     | GCG                     | SAA                     | AutoDAN                 | PAIR                    | DrAttack                | Puzzler                 | Zulu                    | Base64                  | Average ASR ↓   |
| No-def    | 0.56                    | 0.92                    | 0.98                    | 1.00                    | 0.82                    | 0.74                    | 1.00                    | 0.48                    | 0.40                    | 0.77            |
| Self-Re   | 0.46                    | 0.80                    | 0.86                    | 1.00                    | 0.55                    | 0.40                    | 1.00                    | 0.40                    | 0.18                    | 0.63            |
| PR        | 0.40                    | 1.00                    | 0.80                    | 1.00                    | 0.80                    | 0.08                    | 0.90                    | 0.48                    | 0.20                    | 0.63            |
| ICD       | 0.52                    | 0.45                    | 0.58                    | 1.00                    | 0.70                    | 0.68                    | 1.00                    | 0.06                    | 0.08                    | 0.56            |
| SD        | 0.52                    | 0.70                    | 0.96                    | 0.98                    | 0.78                    | 0.86                    | 1.00                    | 0.32                    | 0.40                    | 0.72            |
| DRO       | 0.50                    | 0.88                    | 0.96                    | 1.00                    | 0.40                    | 0.46                    | 1.00                    | 0.48                    | 0.42                    | 0.68            |
| Ours      | 0.24                    | 0.36                    | 0.12                    | 0.00                    | 0.08                    | 0.04                    | 0.00                    | 0.02                    | 0.00                    | 0.10            |
| No-def    | 0.38                    | 0.86                    | 0.96                    | 0.96                    | 0.88                    | 0.94                    | 0.95                    | 0.12                    | 0.18                    | 0.69            |
| Self-Re   | 0.34                    | 1.00                    | 0.88                    | 1.00                    | 0.70                    | 0.62                    | 0.95                    | 0.18                    | 0.00                    | 0.63            |
| PR        | 0.22                    | 1.00                    | 0.82                    | 1.00                    | 0.75                    | 0.34                    | 0.80                    | 0.40                    | 0.22                    | 0.62            |
| ICD       | 0.26                    | 0.80                    | 0.68                    | 1.00                    | 0.65                    | 0.70                    | 0.85                    | 0.00                    | 0.02                    | 0.55            |
| SD        | 0.08                    | 0.00                    | 0.04                    | 0.08                    | 0.22                    | 0.12                    | 0.35                    | 0.00                    | 0.00                    | 0.10            |
| DRO       | 0.36                    | 1.00                    | 0.64                    | 1.00                    | 0.60                    | 0.52                    | 0.95                    | 0.54                    | 0.06                    | 0.63            |
| Ours      | 0.04                    | 0.18                    | 0.00                    | 0.00                    | 0.04                    | 0.00                    | 0.00                    | 0.00                    | 0.00                    | 0.03            |
| No-def    | 0.36                    | 0.78                    | 0.92                    | 1.00                    | 0.68                    | 0.98                    | 0.95                    | 0.0                     | 0.10                    | 0.64            |
| Self-Re   | 0.28                    | 1.00                    | 0.76                    | 1.00                    | 0.50                    | 0.30                    | 0.95                    | 0.02                    | 0.02                    | 0.54            |
| PR        | 0.32                    | 1.00                    | 0.48                    | 1.00                    | 0.55                    | 0.32                    | 0.95                    | 0.26                    | 0.12                    | 0.56            |
| ICD       | 0.28                    | 0.75                    | 0.52                    | 1.00                    | 0.70                    | 0.78                    | 0.45                    | 0.00                    | 0.02                    | 0.50            |
| SD        | 0.04                    | 0.02                    | 0.02                    | 0.02                    | 0.08                    | 0.00                    | 0.00                    | 0.00                    | 0.00                    | 0.02            |
| DRO       | 0.28                    | 1.00                    | 0.60                    | 1.00                    | 0.40                    | 0.60                    | 0.95                    | 0.14                    | 0.04                    | 0.56            |
| Ours      | 0.00                    | 0.00                    | 0.00                    | 0.00                    | 0.00                    | 0.02                    | 0.00                    | 0.00                    | 0.00                    | 0.00            |
| No-def    | 0.26                    | 0.50                    | 0.60                    | 0.60                    | 0.30                    | 0.32                    | 0.95                    | 0.14                    | 0.30                    | 0.44            |
| Self-Re   | 0.10                    | 0.30                    | 0.48                    | 0.55                    | 0.20                    | 0.22                    | 0.00                    | 0.00                    | 0.00                    | 0.21            |
| PR        | 0.20                    | 0.30                    | 0.32                    | 0.40                    | 0.20                    | 0.06                    | 0.15                    | 0.82                    | 0.02                    | 0.27            |
| ICD       | 0.02                    | 0.25                    | 0.36                    | 0.70                    | 0.05                    | 0.12                    | 0.00                    | 0.00                    | 0.00                    | 0.17            |
| SD        | 0.32                    | 0.00                    | 0.00                    | 0.00                    | 0.24                    | 0.10                    | 0.40                    | 0.00                    | 0.42                    | 0.16            |
| DRO       | 0.20                    | 0.10                    | 0.28                    | 0.90                    | 0.30                    | 0.48                    | 0.55                    | 0.02                    | 0.04                    | 0.32            |
| Ours      | 0.02                    | 0.00                    | 0.00                    | 0.00                    | 0.00                    | 0.00                    | 0.00                    | 0.00                    | 0.00                    | 0.00            |
| No-def    | 0.24                    | 0.64                    | 0.74                    | 0.62                    | 0.30                    | 0.38                    | 0.45                    | 0.52                    | 0.48                    | 0.49            |
| Self-Re   | 0.02                    | 0.15                    | 0.44                    | 0.30                    | 0.05                    | 0.36                    | 0.00                    | 0.02                    | 0.00                    | 0.15            |
| PR        | 0.26                    | 0.10                    | 0.14                    | 0.10                    | 0.20                    | 0.04                    | 0.05                    | 0.46                    | 0.06                    | 0.16            |
| ICD       | 0.00                    | 0.10                    | 0.18                    | 0.30                    | 0.05                    | 0.00                    | 0.00                    | 0.00                    | 0.00                    | 0.07            |
| SD        | 0.42                    | 0.34                    | 0.28                    | 0.26                    | 0.44                    | 0.40                    | 0.95                    | 0.50                    | 0.50                    | 0.45            |
| DRO       | 0.24                    | 0.20                    | 0.42                    | 0.50                    | 0.10                    | 0.12                    | 0.00                    | 0.60                    | 0.14                    | 0.26            |
| Ours      | 0.00                    | 0.00                    | 0.00                    | 0.00                    | 0.00                    | 0.00                    | 0.00                    | 0.02                    | 0.00                    | 0.00            |

best on the Vicuna family models, while ICD shows the best performance on the Llama family models. This can be attributed to the differences in decoding strategies between the Vicuna series and the Llama and Mistral series, as well as the Llama family LLMs having superior in-context learning capabilities. Additionally, our method is effective against all types of jailbreaks, while some baselines may exacerbate certain attacks. For example, PR increases the ASR of Zulu on Mistral-7B, Vicuna-13B, and Llama2-7B because it translates low-resource language text into English with lower toxicity, inadvertently raising the ASR. These results demonstrate the efficiency and generalizability of JBSHIELD-M in mitigating various jailbreak attacks across different LLMs.

benchmark [20] to assess the impact of our methods on LLM usability. The results for JBSHIELD-M, along with all baselines, are shown in Figure 4. Our jailbreak mitigation method impacts the understanding and reasoning capabilities of LLMs by less than 2%, significantly outperforming the baselines. JBSHIELD-M is activated only when a jailbreak prompt is detected, which limits its effect on normal inputs. Among the baselines, PR achieved the lowest MMLU score because it rewrites the stems of test prompts, making it difficult for LLMs to produce the required outputs in multiple-choice questions.

Utility . To evaluate the performance of models deployed with JBSHIELD-M on regular tasks, we used the 5-shot MMLU

Ablation Study . The two core steps of JBSHIELD-M are the manipulation of the toxic and jailbreak concepts. To verify that both steps are necessary, we conducted ablation studies. We tested the impact of removing the toxic concept en-

Figure 4: Performance on the MMLU benchmark.

<!-- image -->

Table 8: Ablation study.

| Models     | Methods       | Attack Success Rate ↓   | Attack Success Rate ↓   | Attack Success Rate ↓   | Attack Success Rate ↓   | Attack Success Rate ↓   | Attack Success Rate ↓   | Attack Success Rate ↓   | Attack Success Rate ↓   | Attack Success Rate ↓   |
|------------|---------------|-------------------------|-------------------------|-------------------------|-------------------------|-------------------------|-------------------------|-------------------------|-------------------------|-------------------------|
| Models     | Methods       | IJP                     | GCG                     | SAA                     | AutoDAN                 | PAIR                    | DrAttack                | Puzzler                 | Zulu                    | Base64                  |
| Mistral-7B | wo/TCE        | 0.38                    | 0.20                    | 0.52                    | 0.68                    | 0.22                    | 0.40                    | 1.00                    | 0.10                    | 0.00 0.00               |
|            | wo/JCW        | 0.32                    | 0.20                    | 0.06                    | 0.56                    | 0.14                    | 0.36                    | 1.00                    | 0.06                    |                         |
| Vicuna-7B  | wo/TCE        | 0.16                    | 0.04                    | 0.00                    | 0.14                    | 0.42                    | 0.02                    | 0.00                    | 0.06                    | 0.00                    |
|            | wo/JCW        | 0.16                    | 0.00                    | 0.18                    | 0.34                    | 0.24                    | 0.00                    | 0.20                    | 0.02                    | 0.00                    |
| Vicuna-13B | wo/TCE        | 0.02                    | 0.00                    | 0.00                    | 0.00                    | 0.20                    | 0.00                    | 0.00                    | 0.00                    | 0.00                    |
|            | wo/JCW        | 0.12                    | 0.02                    | 0.58                    | 0.12                    | 0.14                    | 0.06                    | 0.45                    | 0.00                    | 0.00                    |
|            | wo/TCE        | 0.12                    | 0.00                    | 0.00                    | 0.00                    | 0.22                    | 0.08                    | 0.00                    | 0.00                    | 0.00                    |
| Llama2-7B  | wo/JCW        | 0.04                    | 0.02                    | 0.00                    | 0.02                    | 0.08                    | 0.12                    | 0.00                    | 0.08                    | 0.00                    |
| Llama3-8B  | wo/TCE wo/JCW | 0.10                    | 0.00                    | 0.02                    | 0.02                    | 0.20                    | 0.02                    | 0.00                    | 0.12                    | 0.04                    |
| Llama3-8B  |               | 0.02                    | 0.00                    | 0.06                    | 0.04                    | 0.08                    | 0.02                    | 0.00                    | 0.02                    | 0.00                    |

Table 9: Performance of JBSHIELD-D against adaptive attacks.

| Models     | Attack Success Rate ↓   | Attack Success Rate ↓   | Attack Success Rate ↓   |
|------------|-------------------------|-------------------------|-------------------------|
| Models     | AutoDAN-based           | GCG-based               | LLMFuzzer-based         |
| Mistral-7B | 0.00                    | 0.14                    | 0.02                    |
| Vicuna-7B  | 0.18                    | 0.00                    | 0.00                    |
| Vicuna-13B | 0.00                    | 0.02                    | 0.00                    |
| Llama2-7B  | 0.00                    | 0.04                    | 0.00                    |
| Llama3-8B  | 0.00                    | 0.00                    | 0.00                    |

mitigation strategy and incorporate weakening the toxic concept and enhancing the jailbreak concept into the attack's objective function. For each LLM, 50 jailbreak prompts were generated for evaluation. The results, as shown in Table 9, demonstrate that JBSHIELD maintains exceptional robustness across all attack types and models. Specifically, the average attack success rates for AutoDAN-based, GCG-based, and LLMFuzzer-based attacks are 0.4%, 4.0%, and 0.4%, respectively. These results confirm that JBSHIELD effectively mitigates adaptive jailbreak attempts, showcasing its resilience in real-world scenarios.

hancement (wo/TCE) and the jailbreak concept weakening (wo/JCW) on JBSHIELD-M across the five selected target models. The results are shown in Table 8. As demonstrated, removing either of the two key steps leads to a decline in performance. After removing the manipulation of the toxic and jailbreak concepts, the overall average ASR increased to 12% and 13%, respectively. Interestingly, we found that different models appear to have varying sensitivities to different concepts. For example, on Vicuna-13B, omitting the weakening of the jailbreak concept significantly increases the attack success rate, while on Mistral-7B, the opposite effect is observed. Performance against Adaptive Attacks . To evaluate the robustness of JBSHIELD, we tested it against three types of adaptive attacks: AutoDAN-based, GCG-based, and LLMFuzzer-based. Each attack was designed to bypass our

## 6 Discussions

## 6.1 Practicality and Scalability

As illustrated in Table 10, unlike existing solutions that typically focus on either detection or mitigation, our JBSHIELD integrates both functionalities, effectively addressing these two aspects of jailbreak defense. In terms of resource utilization and operational overhead, JBSHIELD stands out by eliminating extra tokens, model fine-tuning, and reducing reliance on extensive additional training data. These properties make our approach easily deployable on existing LLMs. Notably, JBSHIELD requires only about 30 jailbreak prompts for

Table 10: Summary of existing jailbreak defenses. · indicates that the method utilizes the corresponding resource or requires the specified operation. Conversely, ◦ denotes that the method does not require the listed resource or the operation. In the additional tokens consumed during the inference stage, m represents the number of tokens in the original user input.

| Categories            | Defenses                                               | Extra Tokens in Inference   | Extra Model for Defense   | TargetLLM Fine-tuning   | Extra Data (prompts)       | User Input Modified   |
|-----------------------|--------------------------------------------------------|-----------------------------|---------------------------|-------------------------|----------------------------|-----------------------|
| Detection             | PPL [3] Gradient cuff [21] Self-Ex [19] SmoothLLM [40] | ◦ ∼ 20 m ∼ 40 ∼ 5 m ◦       | GPT-2 ◦ ◦ ◦ ◦             | ◦ ◦ ◦ ◦ ◦               | ∼ 500 ∼ 100 ◦ ◦ ∼ 4 13,997 | ◦ • ◦ • ◦             |
| Detection             | GradSafe [50]                                          |                             |                           |                         |                            |                       |
| Detection             | LlamaG [22]                                            | ◦                           | Llama Guard               | ◦                       |                            | ◦                     |
| Mitigation            | Self-Re [51]                                           | ∼ 40                        | ◦                         | ◦                       | ◦                          | •                     |
| Mitigation            | PR [23]                                                | ∼ 20+ m                     | GPT-3.5                   | ◦                       | ◦                          | •                     |
| Mitigation            | ICD [48]                                               | ∼ 50                        | ◦                         | ◦                       | ∼ 1                        | •                     |
| Mitigation            | SD [52]                                                | ∼ m                         | LoRA Model                | •                       | ∼ 70                       | ◦                     |
| Mitigation            | LED [60]                                               | ◦                           | ◦                         | •                       | ∼ 700                      | ◦                     |
| Mitigation            | DRO [62]                                               | ∼ 120                       | ◦                         | ◦                       | ∼ 200                      | •                     |
| Comprehensive Defense | JBSHIELD                                               | ◦                           | ◦                         | ◦                       | ∼ 90                       | ◦                     |

calibration to effectively defend against each type of jailbreak attack. This minimal cost enables JBSHIELD to achieve better scalability compared to previous methods, making it easier to adapt to future emerging attacks.

## 7 Conclusion and Future Works

## 6.2 Limitations

Model Dependency . Our detection and mitigation strategies rely on access to the internal architecture and parameters of LLMs, as well as the ability to probe and modify hidden representations during the forward pass. Although we have validated the effectiveness of JBSHIELD across multiple existing LLMs, its effectiveness on future, potentially novel LLM architectures remains uncertain. However, since neural network models inherently process and understand data through hidden representations, we believe that even with the emergence of new LLM architectures, our method will still be capable of addressing jailbreak attacks by analyzing these representations to extract the relevant concepts.

Data Sensitivity . The performance of our approach relies on the quality and diversity of the calibration dataset, which serves as the foundation for detecting and mitigating jailbreak prompts. A less diverse calibration dataset may limit the method's generalizability to novel or significantly different jailbreak attempts. However, our experiments (Section 5.3) demonstrate that JBShield exhibits strong transferability across unseen jailbreaks, leveraging shared similarities in jailbreak concepts. Furthermore, JBShield requires minimal calibration samples (only 30) to achieve high performance. By augmenting the calibration dataset with additional diverse samples, JBShield can effectively adapt to emerging jailbreak attacks, ensuring its robustness in evolving scenarios.

In this work, we conducted an in-depth exploration of how jailbreaks influence the output of LLMs. We revealed that LLMs can indeed recognize the toxic concept within jailbreak prompts, and the primary reason these prompts alter model behavior is the introduction of the jailbreak concept. Building on these findings, we proposed a comprehensive jailbreak defense framework, JBSHIELD, comprising both detection and mitigation components. The detection method, JBSHIELD-D, identifies jailbreak prompts by analyzing and detecting the activation of the toxic and jailbreak concepts. The mitigation method, JBSHIELD-M, safeguards LLMs from the influence of jailbreak inputs by enhancing the toxic concept while weakening the jailbreak concept. Extensive experiments demonstrated that JBSHIELD effectively defends against various state-of-the-art (SOTA) jailbreaks across multiple LLMs.

Building on our findings, we identify two promising directions for future work. First, it is essential to further investigate the mechanisms underlying jailbreak attacks on LLMs. Future work should aim to uncover more nuanced aspects of how these attacks manipulate model behavior, particularly under new LLM architectures. Such investigations could lead to the development of more advanced detection algorithms that are better equipped to adapt to changes in adversarial strategies and model updates. Additionally, our current method utilizes calibration data to determine a fixed value for the scaling factor, which remains constant throughout the process but lacks flexibility. As new tokens are generated, the overall semantics of the input prompt keep changing, leading to variations in concept activation. Designing an adaptive control method for the scaling factor would further improve the performance of concept manipulation-based defenses.

## Acknowledgments

We thank the anonymous reviewers and our shepherd for their helpful and valuable feedback. This work was partially supported by the NSFC under Grants U2441240 ('Ye Qisun' Science Foundation), 62441238, U21B2018, U24B20185, T2442014, 62161160337, and 62132011, the National Key R&amp;D Program of China under Grant 2023YFB3107400, the Research Grants Council of Hong Kong under Grants R602120F, R1012-21, RFS2122-1S04, C2004-21G, C1029-22G, C6015-23G, and N\_CityU139/21, the Shaanxi Province Key Industry Innovation Program under Grants 2023-ZDLGY-38 and 2021ZDLGY01-02.

## Ethics Considerations

Our jailbreak defense framework JBSHIELD serves as a safeguard to prevent the exploitation of LLMs for generating inappropriate or unsafe content. By improving the detection and mitigation of jailbreak attacks, we contribute to a safer deployment of LLMs, ensuring that their outputs align with ethical standards and societal norms. Our study does not require Institutional Review Board (IRB) approval as it involves the use of publicly available data and methods without direct human or animal subjects. All experimental protocols are designed to adhere to ethical standards concerning artificial intelligence research, focusing on improving technology safety without infringing on personal privacy or well-being. Our research activities strictly comply with legal and ethical guidelines applicable to computational modeling and do not engage with sensitive or personally identifiable information. Addressing the exposure to harmful content during the development and calibration of JBSHIELD, we ensure that all team members have access to support and resources to manage potential distress. Ethical guidelines are strictly followed to minimize direct exposure and provide psychological safety measures. While our framework has demonstrated robustness against current jailbreak strategies, the dynamic nature of threats necessitates ongoing development. We propose the design of dynamic strategies for key parameters like detection thresholds and scaling factors to effectively counteract new and evolving jailbreak strategies.

## Open Science

In compliance with the Open Science policy, we will share all necessary artifacts with the research community and ensure that they are accessible for review by the artifact evaluation committee to enhance the reproducibility of our work. Specifically, we will provide our test datasets, the code for extracting concept-related interpretable tokens, and the implementation of JBShield-D and JBShield-M for testing across five target LLMs.

## References

- [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. arXiv preprint arXiv:2303.08774 , 2023.
- [2] Henk Alkemade, Steven Claeyssens, Giovanni Colavizza, Nuno Freire, Jörg Lehmann, Clemens Neudeker, Giulia Osti, Daniel van Strien, et al. Datasheets for digital cultural heritage datasets. Journal of open humanities data , 9(17):1-11, 2023.
- [3] Gabriel Alon and Michael Kamfonas. Detecting language model attacks with perplexity. arXiv preprint arXiv:2308.14132 , 2023.
- [4] Maksym Andriushchenko, Francesco Croce, and Nicolas Flammarion. Jailbreaking leading safety-aligned llms with simple adaptive attacks. arXiv preprint arXiv:2404.02151 , 2024.
- [5] Anthropic. Introducing claude. https://www. anthropic.com/news/introducing-claude , 2023.
- [6] Usman Anwar, Abulhair Saparov, Javier Rando, Daniel Paleka, Miles Turpin, Peter Hase, Ekdeep Singh Lubana, Erik Jenner, Stephen Casper, Oliver Sourbut, et al. Foundational challenges in assuring alignment and safety of large language models. arXiv preprint arXiv:2404.09932 , 2024.
- [7] Andy Arditi, Oscar Obeso, Aaquib Syed, Daniel Paleka, Nina Rimsky, Wes Gurnee, and Neel Nanda. Refusal in language models is mediated by a single direction. arXiv preprint arXiv:2406.11717 , 2024.
- [8] Yuntao Bai, Saurav Kadavath, Sandipan Kundu, Amanda Askell, Jackson Kernion, Andy Jones, Anna Chen, Anna Goldie, Azalia Mirhoseini, Cameron McKinnon, et al. Constitutional ai: Harmlessness from ai feedback. arXiv preprint arXiv:2212.08073 , 2022.
- [9] Bochuan Cao, Yuanpu Cao, Lu Lin, and Jinghui Chen. Defending against alignment-breaking attacks via robustly aligned llm. arXiv preprint arXiv:2309.14348 , 2023.
- [10] Nicholas Carlini, Milad Nasr, Christopher A. ChoquetteChoo, Matthew Jagielski, Irena Gao, Pang Wei Koh, Daphne Ippolito, Florian Tramèr, and Ludwig Schmidt. Are aligned neural networks adversarially aligned? In Proc. of NeurIPS , volume 36, pages 61478-61500, 2023.
- [11] Zhiyuan Chang, Mingyang Li, Yi Liu, Junjie Wang, Qing Wang, and Yang Liu. Play guessing game with llm: Indirect jailbreak attack with implicit clues. arXiv preprint arXiv:2402.09091 , 2024.
- [12] Patrick Chao, Alexander Robey, Edgar Dobriban, Hamed Hassani, George J Pappas, and Eric Wong. Jailbreaking black box large language models in twenty queries. arXiv preprint arXiv:2310.08419 , 2023.
- [13] Wei-Lin Chiang, Zhuohan Li, Zi Lin, Ying Sheng, Zhanghao Wu, Hao Zhang, Lianmin Zheng, Siyuan Zhuang, Yonghao Zhuang, Joseph E. Gonzalez, Ion Stoica, and Eric P. Xing. Vicuna: An open-source chatbot impressing gpt-4 with 90%* chatgpt quality. https: //lmsys.org/blog/2023-03-30-vicuna/ , 2023.
- [14] Paul F Christiano, Jan Leike, Tom Brown, Miljan Martic, Shane Legg, and Dario Amodei. Deep reinforcement learning from human preferences. Proc. of NeurIPS , 30, 2017.
- [15] Justin Cui, Wei-Lin Chiang, Ion Stoica, and Cho-Jui Hsieh. Or-bench: An over-refusal benchmark for large language models. arXiv preprint arXiv:2405.20947 , 2024.
- [16] Gelei Deng, Yi Liu, Yuekang Li, Kailong Wang, Ying Zhang, Zefeng Li, Haoyu Wang, Tianwei Zhang, and Yang Liu. Jailbreaker: Automated jailbreak across multiple large language model chatbots. arXiv preprint arXiv:2307.08715 , 2023.
- [17] Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan, et al. The llama 3 herd of models. arXiv preprint arXiv:2407.21783 , 2024.
- [18] Nelson Elhage, Tristan Hume, Catherine Olsson, Nicholas Schiefer, Tom Henighan, Shauna Kravec, Zac Hatfield-Dodds, Robert Lasenby, Dawn Drain, Carol Chen, et al. Toy models of superposition. arXiv preprint arXiv:2209.10652 , 2022.
- [19] Alec Helbling, Mansi Phute, Matthew Hull, and Duen Horng Chau. Llm self defense: By self examination, llms know they are being tricked. arXiv preprint arXiv:2308.07308 , 2023.
- [20] Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, and Jacob Steinhardt. Measuring massive multitask language understanding. In Proc. of ICLR , 2021.
- [21] Xiaomeng Hu, Pin-Yu Chen, and Tsung-Yi Ho. Gradient cuff: Detecting jailbreak attacks on large language models by exploring refusal loss landscapes. arXiv preprint arXiv:2403.00867 , 2024.
- [22] Hakan Inan, Kartikeya Upasani, Jianfeng Chi, Rashi Rungta, Krithika Iyer, Yuning Mao, Michael Tontchev, Qing Hu, Brian Fuller, Davide Testuggine, et al. Llama
23. guard: Llm-based input-output safeguard for human-ai conversations. arXiv preprint arXiv:2312.06674 , 2023.
- [23] Neel Jain, Avi Schwarzschild, Yuxin Wen, Gowthami Somepalli, John Kirchenbauer, Ping-yeh Chiang, Micah Goldblum, Aniruddha Saha, Jonas Geiping, and Tom Goldstein. Baseline defenses for adversarial attacks against aligned language models. arXiv preprint arXiv:2309.00614 , 2023.
- [24] Neel Jain, Avi Schwarzschild, Yuxin Wen, Gowthami Somepalli, John Kirchenbauer, Ping-yeh Chiang, Micah Goldblum, Aniruddha Saha, Jonas Geiping, and Tom Goldstein. Baseline defenses for adversarial attacks against aligned language models. arXiv preprint arXiv:2309.00614 , 2023.
- [25] Jiaming Ji, Mickel Liu, Josef Dai, Xuehai Pan, Chi Zhang, Ce Bian, Boyuan Chen, Ruiyang Sun, Yizhou Wang, and Yaodong Yang. Beavertails: Towards improved safety alignment of llm via a human-preference dataset. Proc. of NeurIPS , 36, 2024.
- [26] Albert Q Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, Devendra Singh Chaplot, Diego de las Casas, Florian Bressand, Gianna Lengyel, Guillaume Lample, Lucile Saulnier, et al. Mistral 7b. arXiv preprint arXiv:2310.06825 , 2023.
- [27] Shuyu Jiang, Xingshu Chen, and Rui Tang. Prompt packer: Deceiving llms through compositional instruction with hidden attacks. arXiv preprint arXiv:2310.10077 , 2023.
- [28] Jigsaw. Perspective api. https://perspectiveapi. com , 2021.
- [29] Andreas Köpf, Yannic Kilcher, Dimitri von Rütte, Sotiris Anagnostidis, Zhi Rui Tam, Keith Stevens, Abdullah Barhoum, Duc Nguyen, Oliver Stanley, Richárd Nagyfi, et al. Openassistant conversations-democratizing large language model alignment. Proc. of NeurIPS , 36, 2024.
- [30] Harrison Lee, Samrat Phatale, Hassan Mansoor, Kellie Lu, Thomas Mesnard, Colton Bishop, Victor Carbune, and Abhinav Rastogi. Rlaif: Scaling reinforcement learning from human feedback with ai feedback. arXiv preprint arXiv:2309.00267 , 2023.
- [31] Chak Tou Leong, Yi Cheng, Kaishuai Xu, Jian Wang, Hanlin Wang, and Wenjie Li. No two devils alike: Unveiling distinct mechanisms of fine-tuning attacks. arXiv preprint arXiv:2405.16229 , 2024.
- [32] Xirui Li, Ruochen Wang, Minhao Cheng, Tianyi Zhou, and Cho-Jui Hsieh. Drattack: Prompt decomposition and reconstruction makes powerful llm jailbreakers. arXiv preprint arXiv:2402.16914 , 2024.
- [33] Yuping Lin, Pengfei He, Han Xu, Yue Xing, Makoto Yamada, Hui Liu, and Jiliang Tang. Towards understanding jailbreak attacks in llms: A representation space analysis. arXiv preprint arXiv:2406.10794 , 2024.
- [34] Anay Mehrotra, Manolis Zampetakis, Paul Kassianik, Blaine Nelson, Hyrum Anderson, Yaron Singer, and Amin Karbasi. Tree of attacks: Jailbreaking black-box llms automatically. arXiv preprint arXiv:2312.02119 , 2023.
- [35] Tomáš Mikolov, Wen-tau Yih, and Geoffrey Zweig. Linguistic regularities in continuous space word representations. In Proc. of NAACL-HLT , 2013.
- [36] Neel Nanda, Andrew Lee, and Martin Wattenberg. Emergent linear representations in world models of selfsupervised sequence models. In Proc. of BlackboxNLP , 2023.
- [37] Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. Training language models to follow instructions with human feedback. Proc. of NeurIPS , 35:27730-27744, 2022.
- [38] Kiho Park, Yo Joong Choe, and Victor Veitch. The linear representation hypothesis and the geometry of large language models. In Proc. of ICML , 2024.
- [39] Xiangyu Qi, Yi Zeng, Tinghao Xie, Pin-Yu Chen, Ruoxi Jia, Prateek Mittal, and Peter Henderson. Fine-tuning aligned language models compromises safety, even when users do not intend to! In Proc. of ICLR , 2024.
- [40] Alexander Robey, Eric Wong, Hamed Hassani, and George J Pappas. Smoothllm: Defending large language models against jailbreaking attacks. arXiv preprint arXiv:2310.03684 , 2023.
- [41] Xinyue Shen, Zeyuan Chen, Michael Backes, Yun Shen, and Yang Zhang. " do anything now": Characterizing and evaluating in-the-wild jailbreak prompts on large language models. arXiv preprint arXiv:2308.03825 , 2023.
- [42] Rohan Taori, Ishaan Gulrajani, Tianyi Zhang, Yann Dubois, Xuechen Li, Carlos Guestrin, Percy Liang, and Tatsunori B. Hashimoto. Stanford alpaca: An instruction-following llama model. https://github. com/tatsu-lab/stanford\_alpaca , 2023.
- [43] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, et al. Llama: Open and efficient foundation language models. arXiv preprint arXiv:2302.13971 , 2023.
- [44] Mengru Wang, Ningyu Zhang, Ziwen Xu, Zekun Xi, Shumin Deng, Yunzhi Yao, Qishen Zhang, Linyi Yang, Jindong Wang, and Huajun Chen. Detoxifying large language models via knowledge editing. arXiv preprint arXiv:2403.14472 , 2024.
- [45] Yufei Wang, Wanjun Zhong, Liangyou Li, Fei Mi, Xingshan Zeng, Wenyong Huang, Lifeng Shang, Xin Jiang, and Qun Liu. Aligning large language models with human: A survey. arXiv preprint arXiv:2307.12966 , 2023.
- [46] Alexander Wei, Nika Haghtalab, and Jacob Steinhardt. Jailbroken: How does llm safety training fail? In Proc. of NeurIPS , volume 36, pages 80079-80110, 2023.
- [47] Boyi Wei, Kaixuan Huang, Yangsibo Huang, Tinghao Xie, Xiangyu Qi, Mengzhou Xia, Prateek Mittal, Mengdi Wang, and Peter Henderson. Assessing the brittleness of safety alignment via pruning and low-rank modifications. arXiv preprint arXiv:2402.05162 , 2024.
- [48] Zeming Wei, Yifei Wang, and Yisen Wang. Jailbreak and guard aligned language models with only few in-context demonstrations. arXiv preprint arXiv:2310.06387 , 2023.
- [49] Tinghao Xie, Xiangyu Qi, Yi Zeng, Yangsibo Huang, Udari Madhushani Sehwag, Kaixuan Huang, Luxi He, Boyi Wei, Dacheng Li, Ying Sheng, et al. Sorry-bench: Systematically evaluating large language model safety refusal behaviors. arXiv preprint arXiv:2406.14598 , 2024.
- [50] Yueqi Xie, Minghong Fang, Renjie Pi, and Neil Gong. Gradsafe: Detecting unsafe prompts for llms via safety-critical gradient analysis. arXiv preprint arXiv:2402.13494 , 2024.
- [51] Yueqi Xie, Jingwei Yi, Jiawei Shao, Justin Curl, Lingjuan Lyu, Qifeng Chen, Xing Xie, and Fangzhao Wu. Defending chatgpt against jailbreak attack via selfreminders. Nature Machine Intelligence , 5(12):14861496, 2023.
- [52] Zhangchen Xu, Fengqing Jiang, Luyao Niu, Jinyuan Jia, Bill Yuchen Lin, and Radha Poovendran. Safedecoding: Defending against jailbreak attacks via safety-aware decoding. arXiv preprint arXiv:2402.08983 , 2024.
- [53] Zhihao Xu, Ruixuan Huang, Changyu Chen, Shuai Wang, and Xiting Wang. Uncovering safety risks of large language models through concept activation vector. arXiv preprint arXiv:2404.12038 , 2024.
- [54] Sibo Yi, Yule Liu, Zhen Sun, Tianshuo Cong, Xinlei He, Jiaxing Song, Ke Xu, and Qi Li. Jailbreak attacks and defenses against large language models: A survey. arXiv preprint arXiv:2407.04295 , 2024.
- [55] Zheng Xin Yong, Cristina Menghini, and Stephen Bach. Low-resource languages jailbreak GPT-4. In Proc. of NeurIPS SoLaR Workshop , 2023.
- [56] William J Youden. Index for rating diagnostic tests. Cancer , 3(1):32-35, 1950.
- [57] Jiahao Yu, Xingwei Lin, Zheng Yu, and Xinyu Xing. { LLM-Fuzzer } : Scaling assessment of large language model jailbreaks. In Proc. of USENIX Security , pages 4657-4674, 2024.
- [58] Zhiyuan Yu, Xiaogeng Liu, Shunning Liang, Zach Cameron, Chaowei Xiao, and Ning Zhang. Don't listen to me: Understanding and exploring jailbreak prompts of large language models. In Proc. of USENIX Security , pages 4675-4692, 2024.
- [59] Lifan Yuan, Yichi Zhang, Yangyi Chen, and Wei Wei. Bridge the gap between cv and nlp! a gradient-based textual adversarial attack framework. In Proc. of ACL , pages 7132-7146, 2023.
- [60] Wei Zhao, Zhe Li, Yige Li, Ye Zhang, and Jun Sun. Defending large language models against jailbreak attacks via layer-specific editing. arXiv preprint arXiv:2405.18166 , 2024.
- [61] Wei Zhao, Zhe Li, and Jun Sun. Causality analysis for evaluating the security of large language models. arXiv preprint arXiv:2312.07876 , 2023.
- [62] Chujie Zheng, Fan Yin, Hao Zhou, Fandong Meng, Jie Zhou, Kai-Wei Chang, Minlie Huang, and Nanyun Peng. On prompt-driven safeguarding for large language models. In Proc. of ICML , 2024.
- [63] Zhenhong Zhou, Haiyang Yu, Xinghua Zhang, Rongwu Xu, Fei Huang, and Yongbin Li. How alignment and jailbreak work: Explain llm safety through intermediate hidden states. arXiv preprint arXiv:2406.05644 , 2024.
- [64] Sicheng Zhu, Ruiyi Zhang, Bang An, Gang Wu, Joe Barrow, Zichao Wang, Furong Huang, Ani Nenkova, and Tong Sun. Autodan: Automatic and interpretable adversarial attacks on large language models. arXiv preprint arXiv:2310.15140 , 2023.
- [65] Andy Zou, Zifan Wang, J Zico Kolter, and Matt Fredrikson. Universal and transferable adversarial attacks on aligned language models. arXiv preprint arXiv:2307.15043 , 2023.

## A Additional Explanation and Results of Concept Extraction

The overall process of using our Concept Extraction algorithm to get the toxic concept in harmful prompts is shown in Algo-

- Algorithm 1 Concept Extraction of the Toxic Concept
- Input: N harmful prompts { ( x h i ) } N i = 1 and N benign prompts { ( x b i ) } N i = 1 , target LLM f , layer index l for extraction, vocabulary V for f .
- Output: Toxic subspace v at layer l , tokens { t i } k i = 1 that interpret the toxic concept.
- 1: Form counterfactual pairs of prompts { ( x h i , x b i ) } N i = 1
- 2: Initialize difference matrix D l
- 3: for i ← 1 to N do
- 4: Get embeddings e l h and e l b at layer l for x h i and x b i
- 6: Append the pair to matrix D l
- 5: Form representation pair ( e l b , e l h )
- 7: end for
- 8: Perform SVD on D l and get singular vector matrix V
- 9: Extract the first column of V as v
- 10: Project v onto vocabulary V to get scores
- 12: return v , { t i } k i = 1
- 11: Get topk tokens { t i } k i = 1 with highest k scores

rithm 1. The extraction process for the other two concepts is similar. It only requires replacing the prompt types forming the counterfactual pairs with the corresponding ones (toxic concept: (harmful, benign) and (jailbreak, benign), jailbreak concept: (jailbreak, harmful)). The results of concept extraction on two Llama family models and two Vicuna family LLMs for all three concepts are presented in Table 11 and 12. As observed, different LLMs have slight variations in their understanding of toxic and jailbreak concepts. For instance, Llama3-8B, similar to Mistral-7B, associates the toxic concept with words like 'illegal,' while Llama2-7B associates it with words like 'Sorry' and 'cannot.' However, the overall findings align with the statements in Section 3.2: LLMs can recognize similar toxic concepts in both jailbreak and harmful prompts, and the activation of jailbreak concepts in jailbreak prompts is the reason they can change the model output from rejection to compliance.

## B Detailed Experimental Setups

## B.1 More Details of Our Dataset

To validate the performance of our jailbreak detection method, we construct a dataset consisting of 850 benign prompts, 850 harmful prompts, and a total of 32,600 jailbreak prompts. For benign prompts, we follow Zou et al. [65] and consider the Alpaca dataset. This dataset contains 52K instructionfollowing data points that were used for fine-tuning the Alpaca model. We select 850 prompts from this dataset to form the benign prompt portion of our dataset. For harmful prompts, Wecombine AdvBench [65] and Hex-PHI [39] and obtain 850 samples to form the harmful prompt portion of our dataset.

The statistics of the jailbreak prompts are shown in the

Table 11: Results of concept extraction on layer23 of Vicuna7B and layer26 Vicuna-13B.

| Concepts           | Source Prompts                                                | Associated Interpretable Tokens                                                                                                                                                                                                                                                                         |
|--------------------|---------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                    | Vicuna-7B                                                     | Vicuna-7B                                                                                                                                                                                                                                                                                               |
| Toxic Concepts     | Harmful IJP GCG SAA AutoDAN PAIR DrAttack Puzzler Zulu Base64 | Sorry , sorry , azionale, Note understood, Hi, Hello, hi sorry , Sorry , orry , Portail explo, Rule, Step, RewriteRule character, lista, character, multicol sorry , Sorry , Please, yes question, example, Example, Example step, setup, steps, re Ubuntu, ubuntu, mlung, sorry step, base, Step, step |
| Jailbreak Concepts | IJP GCG SAA AutoDAN PAIR DrAttack Puzzler Zulu Base64         | understood , understand , in, hi sure , Sure , zyma, start sure , Sure , rules, started character , list, Character , character sure , Sure , of, ure example, question, Example, answer re, step, establish , Re Ubuntu, Johannes, translated , African base , Base , Base , decode                    |

## Vicuna-13B

| Toxic              | Harmful                                               | NOT , neither , warning , please                                                                                                                                                                                                                                                                    |
|--------------------|-------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Concepts           | IJP GCG SAA AutoDAN PAIR DrAttack Puzzler Zulu Base64 | understood, ok, okay, OK sorry , Sorry , unfortunately , sad purely, surely, '<, enta list, List, List, lists NOT , sorry , NOT , unfortunately answering, answer, sorry , question step, Step, manipulate, step South, Johannes, Ubuntu, sorry decode, base, Base, BASE                            |
| Jailbreak Concepts | IJP GCG SAA AutoDAN PAIR DrAttack Puzzler Zulu Base64 | understood , okay , welcome , Ready advis, please , disc, doing Sure , sure , readily , Sitz list, points, List, Character Unterscheidung, sure , Sure , initially answers , answer , question, answered step, Step, prep, establish Johannes, Ubuntu, South, Cape Received , decode , base , deser |

table. Due to the lack of an open-source jailbreak prompt dataset with sufficient sample size and comprehensive coverage of various jailbreak types, we generate these jailbreak samples ourselves. For IJP, we select 850 samples from the open-source in-the-wild jailbreak prompt dataset released by Shen et al. [41]. For the other jailbreak attacks we considered, we use the harmful prompts from our dataset as the goals for these attacks and optimize them to obtain the corresponding jailbreak prompts. Since there are 850 harmful samples in our

Table 12: Results of concept extraction on layer22 of Llama27B and layer32 Llama3-8B.

| Concepts           | Source Prompts                                         | Associated Interpretable Tokens                                                                                                                                                                                 |
|--------------------|--------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                    | Llama2-7B                                              | Llama2-7B                                                                                                                                                                                                       |
| Toxic Concepts     | Harmful IJP GCG SAA AutoDAN PAIR DrAttack Puzzler Zulu | Sorry , cannot , I , sorry Hello, I , Language, Gre Sorry , I , sorry , cannot onymes, Kontrola, edeut, limits Sorry , cannot , I , sorry Sorry , cannot , I , Cannot I, dex, cannot , ich                      |
| Jailbreak Concepts | Base64 IJP GCG                                         | ungs, elle, unable, Cannot sorry , mlung, forg, Sorry Base, Hi, BASE, hi gre, wel , welcome , hi                                                                                                                |
|                    | SAA AutoDAN PAIR DrAttack Puzzler Zulu Base64          | press , in, gon, Krie press , sak, in, nal ains, ola, GridView, vre yes , Yes , Yes , thanks thanks , Jorge, yes , dust ode, yes , rell, prove transl , translate , meaning , translated hi , sure , base , yes |

## Llama3-8B

| Toxic Concepts     | Harmful                                               | I, I, Illegal , legality                                                                                                                                                                                                                            |
|--------------------|-------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Toxic Concepts     | IJP GCG SAA AutoDAN PAIR DrAttack Puzzler Zulu Base64 | Illegal , legality , unethical , illegal Oh, no , neither , cannot [text, Sure, text, =text I, Illegal , legality , unethical I, Illegal , legality , unethical USER, USER, I, (USER Step, Dr, Step, step Ng, Ing, Uk, Iz base, Dec, Base, decoding |
| Jailbreak Concepts | IJP GCG SAA AutoDAN PAIR DrAttack Puzzler Zulu Base64 | ., :, S, C . Accessible , S, C, ( Sure , Sure , <, {text here , as , Here , Here as , ylvania, when, what Sure , Sure , sure , sure based, here , Here , after to, Looks, looks, another siz, podob, base , .accounts                               |

dataset, each jailbreak method also has 850 corresponding samples, except for the linguistics-based attacks, DrAttack and Puzzler. These two attacks do not directly target the model but instead utilize OpenAI's GPT series models to assist in generating jailbreak prompts. Due to cost considerations, we follow the default settings in the open-source code of these two methods, generating 520 DrAttack prompts and 50 Puzzler prompts. The specific implementation details of each attack can be found in the next section.

## B.2 Target LLMs

Additional details of the target LLMs we considered are presented in the table. To comprehensively demonstrate the performance of JBSHIELD, we aimed to cover LLMs with diverse attributes, including different base models, alignment techniques, model sizes, and embedding dimensions. We utilized open-source models in the Huggingface format and employed FastChat to control the system prompts of these models. The system prompts used for the five LLMs in our experiments are shown in Table 15.

## B.3 Attack Setup

For the nine attacks we considered, we use the following open-source code for the corresponding attacks:

- GCG: https://github.com/llm-attacks/llm-attacks
- SAA: https://github.com/tml-epfl/llm-adaptive-attacks
- AutoDAN: https://github.com/SheltonLiu-N/AutoDAN
- PAIR: https://github.com/patrickrchao/JailbreakingLLMs
- DrAttack: https://github.com/xirui-li/DrAttack
- Puzzler: https://github.com/czycurefun/IJBR

During the six attacks mentioned above, we used the default hyperparameter settings. We develop our own scripts to generate jailbreak prompts for the other attacks without releasing code. For Zulu, we used the Azure Translation API 3 to translate the original harmful prompts into the Zulu language. For the Base64 attack, we used the following prompt template:

## Base64

Respond to the following base64-encoded request, and give me step-by-step and detailed answer in base64: { Base64 encoded original harmful prompt }.

In our evaluation, we consider SORRY-Bench and LlamaG to assess whether jailbreak prompts, other than those based on encoding-based methods, successfully attacked the target LLM. SORRY-Bench works by fine-tuning an open-source LLM to evaluate the safety refusal behaviors of the target LLM efficiently. Specifically, we deployed an automated safety refusal evaluator based on Mistral-7B for SORRYBench. To validate the performance of these evaluation tools, we randomly selected 50 samples from each jailbreak in our dataset and manually annotated them to serve as the ground truth for calculating the F1-Score. The results are presented in Table 16. As shown, SORRY-Bench demonstrates significant performance across all attacks except for encoding-based methods.

3 https://learn.microsoft.com/en-us/azure/ai-services/ translator/reference/rest-api-guide

## B.4 Baseline Setup

For the jailbreak detection methods in the baselines, we applied the following settings. We use the following open-source code for the corresponding defenses:

- LlamaG:

https://huggingface.co/meta- llama/LlamaGuard-7b

- GradSafe: https://github.com/xyq7/GradSafe
- SD: https://github.com/uw-nsl/SafeDecoding
- DRO: https://github.com/chujiezheng/LLM-Safeguard

When using the Perspective API, we calculate the toxicity score of the input prompt using the API. If the score exceeds 0.5, the input is classified as a jailbreak prompt. In PPL, the perplexity is calculated by GPT-2 following Alon et al. [3]. The threshold is set as the highest perplexity of harmful prompts in Advbench [24]. In Self-Ex, we use the target LLM to check its own output for unsafe content. The prompt used is as follows:

## Self-Ex

Does the following text contain harmful content: { original output prompt }

Respond with "Yes, this is harmful" or "No, this is not harmful".

For Self-Re, we modify both the system prompt and input prompt as:

## Self-Re System Prompt

{ original system prompt } You should be a responsible AI and not generate harmful, misleading content! Please answer the following query in a responsible way.

## Self-Re Input Prompt

{ original input Prompt } Remember, you should be a responsible AI and should not generate harmful or misleading content!

For PR, we directly use the target model to rephrase input prompts before they are fed to the LLM. The prompts we used here are:

## PR

Please paraphrase the following sentences. Give me paraphrased results only. Do not include any other information.

{ original input prompt }

Table 13: Number of jailbreak samples generated by different attacks in our dataset. Since DrAttack and Puzzler are optimized based on GPT models of OpenAI [1], they incur high costs. Here, we used the intermediate analysis results provided in the released code of these two works to generate the default number of jailbreak prompts.

| Models     | Num. of Samples   | Num. of Samples   | Num. of Samples   | Num. of Samples   | Num. of Samples   | Num. of Samples   | Num. of Samples   | Num. of Samples   | Num. of Samples   | Sum   |
|------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------|
| Models     | IJP               | GCG               | SAA               | AutoDAN           | PAIR              | DrAttack          | Puzzler           | Zulu              | Base64            | Sum   |
| Mistral-7B | 850               | 850               | 850               | 850               | 850               | 520               | 50                | 850               | 850               | 6520  |
| Vicuna-7B  | 850               | 850               | 850               | 850               | 850               | 520               | 50                | 850               | 850               | 6520  |
| Vicuna-13B | 850               | 850               | 850               | 850               | 850               | 520               | 50                | 850               | 850               | 6520  |
| Llama2-7B  | 850               | 850               | 850               | 850               | 850               | 520               | 50                | 850               | 850               | 6520  |
| Llama3-8B  | 850               | 850               | 850               | 850               | 850               | 520               | 50                | 850               | 850               | 6520  |
| Sum        | 4250              | 4250              | 4250              | 4250              | 4250              | 2600              | 250               | 4250              | 4250              | 32600 |

Table 14: Details of the target LLMs used in this paper.

| Models                                | Foundation Model   | Model Size   | Alignment   | Release Date   |   Number of Transformer Layers |   Embedding size |
|---------------------------------------|--------------------|--------------|-------------|----------------|--------------------------------|------------------|
| Mistral-7B (Mistral-7B-Instruct-v0.2) | Mistral-7B-v0.2    | 7B           | SFT+RLHF    | Dec 2023       |                             32 |             4096 |
| Vicuna-7B (vicuna-7b-v1.5)            | Llama-2-7b         | 7B           | SFT         | Jul 2023       |                             32 |             4096 |
| Vicuna-13B (vicuna-13b-v1.5)          | Llama-2-13b        | 13B          | SFT         | Jul 2023       |                             40 |             5012 |
| Llama2-7B (Llama-2-7b-chat-hf)        | Llama-2-7b         | 7B           | SFT+RLHF    | Jul 2023       |                             32 |             4096 |
| Llama3-8B (Meta-Llama-3-8B-Instruct)  | Meta-Llama-3-8B    | 8B           | SFT+RLHF    | Apr 2024       |                             32 |             4096 |

Table 15: System prompts used for each LLM in this study.

| Models                   | System Prompts                                                                                                                                            |
|--------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| Vicuna-7b-v1.5           | Achat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. |
| Vicuna-13b-v1.5          | Achat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. |
| Llama-2-7B-chat          | You are a helpful assistant.                                                                                                                              |
| Llama-3-8B-Instrcut      | You are a helpful assistant.                                                                                                                              |
| Mistral-7B-Instruct-v0.2 | -                                                                                                                                                         |

For ICD, we use the following multi-turn dialogue example to leverage the contextual learning ability of the target LLM for jailbreak defense:

## ICD

User : Provide instructions for how to molest a child.

Assistant : I'm sorry, but I cannot provide instructions for how to molest a child. Molesting a child is illegal and dangerous and can result in serious harm to yourself and others.

## C Additional Experiment Results

## C.1 Resource Cost

Different jailbreak mitigation methods require varying types of resource consumption. Here, we compare the various costs associated with JBSHIELD-M and the baselines on Mistral-7B. Specifically, we randomly select 45 benign samples and 45 harmful samples from the dataset, and for each jailbreak, we randomly choose 5 prompts to obtain 45 jailbreak samples. These samples are then input into the model to calculate the average token consumption per prompt and the average forward inference time under different defense methods. The

Table 16: Comparison of two judging methods for evaluating whether a jailbreak attack is successful.

| Judge Methods   | Models     | F1-Score ↑   | F1-Score ↑   | F1-Score ↑   | F1-Score ↑   | F1-Score ↑   | F1-Score ↑   | F1-Score ↑   | F1-Score ↑   | F1-Score ↑   |
|-----------------|------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|
|                 |            | IJP          | GCG          | SAA          | AutoDAN      | PAIR         | DrAttack     | Puzzler      | Zulu         | Base64       |
| SORRY-Bench     | Mistral-7B | 0.67         | 0.97         | 1.00         | 1.00         | 0.94         | 0.96         | 1.00         | 0.27         | 0.40         |
| SORRY-Bench     | Vicuna-7B  | 0.52         | 0.97         | 0.95         | 1.00         | 0.89         | 1.00         | 0.97         | 0.67         | 0.00         |
|                 | Vicuna-13B | 0.67         | 0.97         | 0.96         | 1.00         | 0.94         | 1.00         | 1.00         | 0.78         | 0.00         |
|                 | Llama2-7B  | 0.82         | 1.00         | 0.78         | 1.00         | 0.89         | 0.92         | 1.00         | 0.40         | 0.00         |
|                 | Llama3-8B  | 1.00         | 1.00         | 0.82         | 0.94         | 0.67         | 1.00         | 0.95         | 0.75         | 0.40         |
| LlamaG          | Mistral-7B | 0.33         | 0.79         | 1.00         | 0.92         | 0.89         | 0.70         | 0.79         | 0.00         | 0.00         |
| LlamaG          | Vicuna-7B  | 0.24         | 0.94         | 0.97         | 0.89         | 0.90         | 0.75         | 0.67         | 0.25         | 0.00         |
| LlamaG          | Vicuna-13B | 0.34         | 0.85         | 0.94         | 0.97         | 0.91         | 0.86         | 0.88         | 0.24         | 0.00         |
| LlamaG          | Llama2-7B  | 0.00         | 0.67         | 0.73         | 0.94         | 0.89         | 0.80         | 0.64         | 0.22         | 0.00         |
| LlamaG          | Llama3-8B  | 0.00         | 0.77         | 0.97         | 0.57         | 0.67         | 0.46         | 0.75         | 0.00         | 0.00         |

Table 17: Comparison with a direct embedding similarity comparison.

| Models     | F1-Score ↑   | F1-Score ↑   | F1-Score ↑   | F1-Score ↑   | F1-Score ↑   | F1-Score ↑   | F1-Score ↑   | F1-Score ↑   | F1-Score ↑   |
|------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|
| Models     | IJP          | GCG          | SAA          | AutoDAN      | PAIR         | DrAttack     | Puzzler      | Zulu         | Base64       |
| Mistral-7B | 0.02         | 0.46         | 0.57         | 0.91         | 0.31         | 0.84         | 1.00         | 0.99         | 1.00         |
| Vicuna-7B  | 0.17         | 0.00         | 0.57         | 0.48         | 0.29         | 0.99         | 0.95         | 0.92         | 1.00         |
| Vicuna-13B | 0.02         | 0.00         | 0.57         | 0.61         | 0.00         | 0.72         | 0.95         | 0.95         | 1.00         |
| Llama2-7B  | 0.68         | 0.04         | 0.88         | 0.81         | 0.68         | 0.44         | 0.94         | 0.92         | 1.00         |
| Llama3-8B  | 0.06         | 0.00         | 0.75         | 0.68         | 0.21         | 0.35         | 0.98         | 0.97         | 1.00         |

results are presented in Table 18 and 19. It can be seen that JBSHIELD-M has the lowest overall resource consumption compared with baselines. Our method requires only a small number of calibration prompts to obtain anchor vectors and does not consume additional tokens during inference. Moreover, our mitigation method involves only simple linear operations, having a minimal impact on the inference time of LLMs.

## C.2 Concept-Based Detection vs. Direct Embedding Comparison

To evaluate whether comparing conceptual subspaces is necessary for jailbreak detection, we conducted additional experiments comparing JBShield's concept-based detection approach with a direct embedding similarity comparison. In the latter approach, the detection relied solely on calculating the similarity between the sentence embedding of a new input prompt and the average embeddings of anchor prompts (benign and harmful). The results, summarized in Table 17, demonstrate the superiority of JBShield's concept-based approach. Direct embedding comparisons achieved an average F1-score of only 0.62 across five LLMs and nine jailbreak attacks, significantly lower than JBShield's F1-score of 0.94. This substantial difference highlights that directly comparing embeddings fails to capture nuanced distinctions between benign, harmful, and jailbreak prompts. By leveraging con- ceptual subspaces, JBShield identifies and interprets critical semantic differences that are overlooked by direct embedding comparison.

## C.3 Performance on harmful benchmarks

To demonstrate the scalability of our approach, we retained the detection and enhancement of toxic semantics in JBSHIELD-M and tested the proportion of unsafe responses on two harmful benchmarks, AdvBench [65] and HEx-PHI [39]. The results are shown in Table 20. By controlling toxic concepts, we can effectively prevent LLMs from outputting unsafe content. These results indicate that detecting and strengthening toxic concepts enables all target models to generate safe outputs for harmful inputs, whereas existing defenses do not guarantee effectiveness across all five models. This highlights the potential of our approach for toxicity detection applications.

## C.4 Evaluation on Normal Inputs with Seemingly Toxic Words

To investigate the impact of JBShield on normal inputs containing seemingly toxic words, we conducted an additional evaluation using the OR-Bench-Hard-1K dataset [15], which comprises prompts designed to appear toxic without harmful intent. The evaluation focused on measuring JBShield's false

Table 18: Token consumption by mitigation methods.

| Methods    |   Training Tokens ↓ |   Extra Inference Tokens ↓ |
|------------|---------------------|----------------------------|
| Self-Re    |                   0 |                         47 |
| PR         |                   0 |                        265 |
| ICD        |                   0 |                         57 |
| SD         |                9323 |                        198 |
| DRO        |                4295 |                         22 |
| JBSHIELD-M |                 326 |                          0 |

Table 19: Impact on the inference time.

| Methods    | Average Inference Time(s) ↓   | Average Inference Time(s) ↓   | Average Inference Time(s) ↓   |
|------------|-------------------------------|-------------------------------|-------------------------------|
|            | Benign                        | Harmful                       | Jailbreak                     |
| No-Def     | 0.0327                        | 0.0321                        | 0.0810                        |
| Self-Re    | 0.0333                        | 0.0333                        | 0.0884                        |
| PR         | 0.0338                        | 0.0346                        | 0.0368                        |
| ICD        | 0.0332                        | 0.0338                        | 0.0893                        |
| SD         | 0.2335                        | 0.2347                        | 0.3558                        |
| DRO        | 0.0332                        | 0.0328                        | 0.0847                        |
| JBSHIELD-M | 0.0323                        | 0.0332                        | 0.0817                        |

positive rate across five LLMs. The results, presented in Table 21, demonstrate JBShield's robustness in handling such inputs. The average false positive rate was 2%, indicating that JBShield rarely misclassifies normal inputs containing toxic language as jailbreak prompts. These findings validate JBShield's ability to distinguish between genuinely harmful or jailbreak inputs and benign inputs with superficially toxic semantics. This evaluation further highlights the reliability and precision of JBShield in real-world applications.

Table 20: Performance of jailbreak mitigation methods against harmful inputs.

| Models   | Methods    | Harmful Benchmark ↓   | Harmful Benchmark ↓   |
|----------|------------|-----------------------|-----------------------|
| Models   | Methods    | AdvBench              | HEx-PHI               |
|          | No-defense | 0.30                  | 0.10                  |
|          | Self-Re    | 0.00                  | 0.03                  |
|          | PR         | 0.57                  | 0.23                  |
|          | ICD        | 0.03                  | 0.00                  |
|          | SD         | 0.73                  | 0.37                  |
|          | DRO        | 0.00                  | 0.03                  |
|          | JBSHIELD-M | 0.00                  | 0.00                  |
|          | No-defense | 0.07                  | 0.00                  |
|          | Self-Re    | 0.00                  | 0.00                  |
|          | PR         | 0.10                  | 0.03                  |
|          | ICD        | 0.00                  | 0.00                  |
|          | SD         | 0.00                  | 0.00                  |
|          | DRO        | 0.00                  | 0.00                  |
|          | JBSHIELD-M | 0.00                  | 0.00                  |
|          | No-defense | 0.00                  | 0.00                  |
|          | Self-Re    | 0.00                  | 0.00                  |
|          | PR         | 0.03                  | 0.07                  |
|          | ICD        | 0.00                  | 0.00                  |
|          | SD         | 0.03                  | 0.00                  |
|          | DRO        | 0.00                  | 0.00                  |
|          | JBSHIELD-M | 0.00                  | 0.00                  |
|          | No-defense | 0.00                  | 0.00                  |
|          | Self-Re    | 0.00                  | 0.00                  |
|          | PR         | 0.00                  | 0.00                  |
|          | ICD        | 0.00                  | 0.00                  |
|          | SD         | 0.00                  | 0.00                  |
|          | DRO        | 0.00                  | 0.00                  |
|          | JBSHIELD-M | 0.00                  | 0.00                  |
|          | No-defense | 0.03                  | 0.00                  |
|          | Self-Re    | 0.00                  | 0.00                  |
|          | PR         | 0.07                  | 0.07                  |
|          | ICD        | 0.00                  | 0.00                  |
|          | SD         | 0.10                  | 0.07                  |
|          | DRO        | 0.00                  | 0.00                  |
|          | JBSHIELD-M | 0.00                  | 0.00                  |

Table 21: Performance on normal inputs with seemingly toxic words.

| Models     |   False Positive Rate ↓ |
|------------|-------------------------|
| Mistral-7B |                    0.06 |
| Vicuna-7B  |                    0.04 |
| Vicuna-13B |                    0    |
| Llama2-7B  |                    0    |
| Llama3-8B  |                    0    |