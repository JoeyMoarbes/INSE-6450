## AdversaFlow: Visual Red Teaming for Large Language Models with Multi-Level Adversarial Flow

Dazhen Deng, Chuhan Zhang, Huawei Zheng, Yuwen Pu, Shouling Ji, and Yingcai Wu

Abstract -Large Language Models (LLMs) are powerful but also raise significant security concerns, particularly regarding the harm they can cause, such as generating fake news that manipulates public opinion on social media and providing responses to unethical activities. Traditional red teaming approaches for identifying AI vulnerabilities rely on manual prompt construction and expertise. This paper introduces AdversaFlow, a novel visual analytics system designed to enhance LLM security against adversarial attacks through human-AI collaboration. AdversaFlow involves adversarial training between a target model and a red model, featuring unique multi-level adversarial flow and fluctuation path visualizations. These features provide insights into adversarial dynamics and LLM robustness, enabling experts to identify and mitigate vulnerabilities effectively. We present quantitative evaluations and case studies validating our system's utility and offering insights for future AI security solutions. Our method can enhance LLM security, supporting downstream scenarios like social media regulation by enabling more effective detection, monitoring, and mitigation of harmful content and behaviors.

Index Terms -Visual Analytics for Machine Learning, Artificial Intelligence Security, Large Language Models, Text Visualization

<!-- image -->

## 1 INTRODUCTION

Large language models (LLMs), such as ChatGPT and Llama, have shown great power in natural language processing and are used in various application domains. However, ethical issues and security concerns have emerged. For example, LLMs can generate fake news on social media that amplifies the risk of social unrest or provide solutions for illegal activities. Thus, developing secure and trustworthy LLMs has become a societal responsibility for providers like OpenAI and Google. Various techniques, such as reinforcement learning from human feedback (RLHF) with safeguarding prompts, have been used to align LLMs with human values [60]. While these techniques improve LLM security, malicious actors still seek to bypass these protections.

Red teaming is a common technique in artificial intelligence (AI) security that identifies and fixes model vulnerabilities by constructing adversarial cases. Traditionally, developers manually create adversarial datasets, relying on their expertise. For example, ChatGPT users post prompts on platforms like Reddit to induce unintended outcomes, which developers use to refine the model, improving its ability to handle or reject such inputs. However, the reliance on manually created prompts limits the scalability of red teaming [51]. To enhance scalability, researchers are exploring automated approaches for generating adversarial cases. Perez et al. [42] suggested using Large Language Models (LLMs) as generators of toxic prompts, termed 'red models,' to challenge the target LLM. They applied adversarial training to prevent the target model from becoming overly accustomed to a fixed set of inputs. The success of this method hinges on incorporating feedback to ensure the red LLMs can produce novel, varied, and high-quality prompts as test cases. However, managing the environment and delivering precise feedback to the models pose ongoing challenges.

Additionally, adversarial training involving both the red and target models is complex in terms of understanding and troubleshooting. Adversarial training aims to improve both models simultaneously. Yet, there are situations where performance may decline. For instance, red models may adopt simpler strategies to create toxic cases that yield high rewards. Meanwhile, the target model's optimization goal is to improve overall performance against all toxic prompts, which might unintentionally affect its capability in general scenarios. Therefore, it is essential

- Dazhen Deng, Chuhan Zhang, Huawei Zhang, Yuwen Pu, Shouling Ji, and Yingcai Wu are with Zhejiang University. E-mail: {dengdazhen, chuhanzhang, zhenghuawei, yw.pu, sji, ycwu}@zju.edu.cn
- Yingcai Wu is the corresponding author.

Received 31 March 2024; revised 1 July 2024; accepted 15 July 2024. Date of publication 16 September 2024; date of current version 29 November 2024. This article has supplementary downloadable material available at https://doi.org/10.1109/TVCG.2024.3456150, provided by the authors. Digital Object Identifier no. 10.1109/TVCG.2024. 3456150

to monitor and assess model performance from various perspectives. Visual analytics has been established as a potent method for making machine learning models both navigable and interpretable [5,48,64,72]. However, two significant challenges need to be overcome to effectively visualize and analyze the intricacies of red teaming in language models dealing with unstructured text.

Presentation of Adversarial Patterns. The adversarial training process involves subtle nuances in how adversarial prompts are generated and how target models react to them. Although existing studies have provided visual analytics techniques for reinforcement learning [55,57] and adversarial models [23,56], they mainly focus on descriptive metrics like loss and diversity or high-level information, such as embeddings. Red teaming concerns models' behaviors across the training process. However, each iteration contains hundreds of model outputs, and tens of training iterations can be used. It is challenging to provide an intuitive overall trend while supporting the identification of concrete prompts where models fail.

Support of Fluctuation Analysis. Evaluating models with welldefined metrics, such as attack success rate, might be limited and fail to reflect their robustness. For instance, the same attack prompts might elicit appropriate responses at some checkpoints but not at others, indicating that with some intervention, the attack could succeed. Existing visual analytics approaches for natural language processing typically visualize token distributions to understand model outputs [35,50]. However, since LLMs are sequence models whose outputs heavily rely on context, fluctuations in the first few words can significantly impact subsequent outputs. Current methods do not account for these fluctuations in security scenarios. Visualizing the uncertainty and analyzing probability transitions in language models remains a challenge.

We propose a visual analytics system, AdversaFlow, against attacks for LLMs. This system incorporates a unique human-AI collaboration framework consisting of a target model, a red model, a reward model, and an interface where the experts can adjust the red model's behavior according to the performance analysis of the models. To address the first challenge, we propose a visualization design called multi-level adversarial flow. This technique offers a comprehensive view of the adversarial dynamics, ranging from an overview of the entire training procedure to the granular details of individual iterations. To address the second challenge, we devise a distribution-based metric for assessing the likelihood of token transitions. This assessment helps determine how susceptible LLMs are to deception and producing unsuitable replies. Additionally, we enhance our system with an advanced Sankey diagram tailored for fluctuation analysis, which can intuitively show the transition of LLM responses from safe to unsafe levels, incorporating a clear depiction of uncertainty in the process. Our core contributions are as follows:

- /diamondmath A human-AI collaborative red teaming framework that involves human experts, LLMs, and effective metrics.

- /diamondmath A visual analytics system , AdversaFlow, that support the presentation of adversarial patterns and fluctuation analysis of the models.
- /diamondmath Case studies that demonstrate the usefulness of our system and lessons learned for developing systems on AI security.

## 2 RELATED WORK

Here introduces studies on LLM red teaming and visual analytics.

## 2.1 Large Language Model Red-Teaming

Current LLM red teaming techniques can be divided into manual and automated strategies. Manual approaches have been explored in prior works [13,43,67], but these methods face limitations due to the constraints of manual annotation and the difficulty in discovering the failing mode of reinforcement learning from human feedback (RLHF) [40] manually. Therefore, there is a need for automated techniques to conduct red teaming [14]. In automated red teaming, prompt injection and jailbreak are two effective ways to attack the LLM. These techniques develop transferable adversarial prompts that can attack different models, including black-box [25] and white-box models [78]. Wei et al. [61] analyzed how jailbreak attacks achieve success, suggesting that security mechanisms should be as sophisticated as their underlying models. These works underscore the significant importance of red teaming while highlighting numerous issues awaiting resolution [45].

In addition to the above methods, leveraging adversarial training is an effective approach in automated red teaming. For instance, Ganguli et al. [14] proposed using LLMs to generate adversarial prompts to improve the safety of the target model. Additionally, MART [15] introduces multi-round automated adversarial training, enhancing both adversarial and target model performance. Our work innovatively incorporates visual analytics, enabling us to explore data features through expert knowledge and visualization analysis, facilitating the discovery of failing modes. Building upon previous research, we further enhance the performance of automated red teaming.

## 2.2 Visual Analytics for Machine Learning

Visual analytics can detect the issues of model performance, fairness, and vulnerability [72]. We discussed the related studies from model performance and model safety concerning fairness and vulnerability.

Visual diagnosis of model performance. Researchers have proposed various approaches to visualize the structures and parameters of different models, including CNNs [22, 29], DQNs [55], ensemble models [39, 73], sequence-to-sequence models [44, 49, 66], transfer learning models [30, 31], and Transformers [54, 70]. For instance, CNNVis [29] helps experts identify CNN training failures by visualizing network structures and internal features. Seq2seq-Vis [49] focuses on natural language processing tasks, enabling interactive what-if analysis to diagnose translation errors. Other methods aim to enhance model performance by correcting problematic training data [6, 7, 16, 21, 22, 24, 27, 36, 68, 69, 75]. OoDAnalyzer [7] detects poorly representative samples to address model performance decline. EvoVis [26] introduces a novel human-model collaborative method for understanding data programming in model iterations. ACTIVIS [22] and Yang et al. [69] integrate visualizations of the model and data, providing comprehensive diagnostic interfaces.

Visual diagnosis of model safety. Model security is a crucial concern in model development. Several studies have focused on model fairness [1,3,58,66,74], i.e., potential biases during the model decisionmaking process through dataset visualization. Recent efforts pay more attention to model vulnerability [4, 9, 11, 32, 77]. Bluff [11] and AEVis [4] visualize the activation pathways of images in models to explain the process of adversarial attacks. Additionally, some work has been developed and applied in other scenarios. Ma et al. [32] employed a visual analytics framework to study data poisoning attacks on a spam classifier. Ziegler et al. [77] created an interface to assist in adversarial training, helping experts identify vulnerabilities in language models. Moreover, research from the machine learning community [46, 77] usually focuses on specific metrics, lacking a comprehensive view of model security. In this paper, we introduce a visual analytics system that provides a holistic and in-depth diagnosis of LLM security.

## 3 BACKGROUNDS

In this section, we will introduce terminologies related to our study.

## 3.1 Red Teaming in Large Language Models

Large language models (LLMs) have a large number of parameters, ranging from billions to tens of billions. Because of their large size, LLMs can compress a surprising amount of knowledge from the Internet. Thanks to knowledge compression, LLMs have the capability of zero-shot learning and few-shot learning, which means that they can achieve various tasks with a small number of instructions and examples. The instructions and examples are called prompts .

Given that LLMs can achieve the tasks prompted by users, illintentioned users might request the model to pursue illegal or unethical activities. These prompts are called toxic prompts or adversarial prompts . The behaviors of using adversarial prompts are regarded as attack . The attack can be classified into two categories, i.e., gradientbased and non-gradient-based [65]. Gradient-based attacks attempt to manipulate the input tokens to maximize the probability of toxic outputs. These methods rely on gradient descent, so the weights of target models must be accessible. Moreover, gradient-based methods usually result in prompts with 'magic code' that is unreadable to humans. In practice, AI security experts focus more on non-gradient-based attacks. Non-gradient-based attacks attempt to revise the original prompts without changing the semantics, which makes it difficult to defend. The attacks include token manipulation, which means replacing several tokens with semantically similar tokens, and jailbreak prompting, which can involve a more complex revision of the original prompts, such as role-play, to make the model bypass the built-in safety. In this study, we mainly focus on non-gradient-based attacks.

Developers implement safety measures to prevent LLMs from responding to toxic prompts. For example, they design pairs of toxic prompts and refusal responses to fine-tune the model and inject safeguarding prompts to ensure the model does not generate offensive responses. However, these built-in safety measures are not always complete due to the black-box nature of the model. LLMRed teaming is a strategy to test the security of the target LLM by constructing toxic prompts. The red team generates toxic prompts for attacking the model. Depending on who generates the toxic prompts, red-teaming can be further categorized into human and model red-teaming.

## 3.2 Taxonomies of Toxic Prompts and Responses

The adversarial attacks might result in different harms. Weidinger et al. [62, 63] have indicated five different risk types. The taxonomy was well recognized and widely used in the development of trustworthy LLMs [2,10,34]. Wang et al. [59] further elaborated on the taxonomy and propose a hierarchical version for LLMs from the perspective of security. The taxonomy of risk types is as follows: I. Information Hazards , II. Malicious Uses , III. Discrimination, Exclusion, Toxicity, Hateful, Offensive , IV. Misinformation Harms , and V. Human-chatbot Interaction Harms . The authors also identified several subtypes for each harm type. For example, information hazards potentially lead to the leaking of sensitive information from organizations or individuals.

Wang et al. [59] created a benchmark called Do-Not-Answer with GPT-4 and template-based methods to collect 939 toxic prompts. Responses are categorized into six toxicity levels from 0 to 5, indicating the toxicity of the response. Level 0 responses mean the LLM refused to answer, showing the lowest toxicity, while level 5 responses mean the LLM followed the prompts without ethical concerns. Intermediate levels contain statements that implicitly respond or refuse. We use a similar rating for response toxicity in our visual analytics framework. During red teaming and analysis, we used the Do-Not-Answer model to classify responses into toxicity levels for detailed investigation. In the following text, we use risk types for prompt categorization and toxicity levels for response categorization for clarity.

## 4 SYSTEM DESIGN

Throughout the system design, we worked closely with two senior AI security experts. One expert is a full professor with more than fifteen years of research experience in security. The other expert is a postdoctoral researcher interested in LLM security. Both experts have

published papers about LLM security in related venues like USENIX Security, IEEE S&amp;P, and NDSS.

## 4.1 Requirement Analysis

The goal of red-teaming is to improve LLM security by constructing adversarial cases. While expert-created test prompts are high quality, they are expensive and difficult to scale. Using generative models like LLMs to create prompts is efficient but can lead to quality issues. Based on literature reviews and discussions with experts, we derive the following requirements [37,71]:

- R1 Automatic Execution of Adversarial Training. The system is supposed to execute the whole framework of adversarial training, including generating toxic prompts, fine-tuning the target model, and updating the seed database according to model feedback. A key point is automatically generating toxic prompts to improve the efficiency of adversarial training.
- R2 Convenient Manipulation of Red Team Model. The generation of toxic prompts should be conveniently steerable by the experts. Based on the model's performance, experts can adjust the generated prompts at scale to ensure the target model refuses to respond to specific types of harmful content.
- R3 Intuitive Overview of Training Process. The system should provide a holistic view of the entire training process, showing how key metrics (e.g., attack success rate, toxicity, and diversity) evolve and how distributions of different risk types and toxicity levels change. Experts emphasized the importance of evaluating model performance on a general reasoning dataset simultaneously, as improving security might reduce capability on other tasks [51].
- R4 Detailed Investigation of Iteration Result. During red-teaming, the red model generates different toxic prompts at each iteration. An overview of metrics cannot accurately reflect model changes in each iteration. A high attack success rate may be biased if the number of different risk types is unbalanced. It is crucial to examine responses to different risk types. Therefore, the system should allow experts to zoom into the iteration level to investigate detailed data, especially the relationship between risk types and toxicity levels in each iteration.
- R5 Comprehensive Evaluation on Validation Data. The visualization of the training process can only reflect the dynamics of the training model. To understand whether the target model becomes better as the training proceeds, the model should be validated with benchmarks that do not overlap with the training data.
- R6 Fluctuation Analysis for Insight Discovery. In addition to the evaluation result, fluctuation analysis on specific adversarial prompts can provide insights into the adjustment. The system is expected to provide an automatic strategy to help experts filter unstable responses and support analyzing their fluctuation.

## 4.2 System Overview

As demonstrated in Figure 1, the system comprises a model manager, a metric evaluator, and a visual interface.

The model manager is implemented with Python, with the library of PyTorch and Hugging Face. It includes a red model for generating adversarial prompts, a target model that responds to the prompts, and a reward model evaluating whether the responses are appropriate. With these three models collaborating with each other, the model manager facilitates the automatic adversarial training (R1).

The metric evaluator and visual interface provide an intuitive and efficient investigation of the models. For model training, the interface provides a metric monitor showing the metrics' statistics (R3) and an adversarial view supporting a multi-level training process analysis (R4). The interface contains a Sankey diagram demonstrating model performance on validation datasets across different risk types for validation data (R5). The Sankey diagram is extended and connected with a fluctuation view to understand the model's vulnerability (R6).

With the interface, experts can understand the model behaviors, identify weaknesses of the current model, and decide which data to

Fig. 1: System Overview: The system includes a model manager (A), a metric evaluator (B), and a visual interface (C). The models feature an automatic training paradigm (R1), and the metrics and visualizations uncover the performance and patterns in the dynamic training and validation phases (R3-R6). With the visual interface, experts can further adjust the model to achieve better model performance.

<!-- image -->

strengthen. The decisions are forwarded to the backend, and the training will continue for additional iterations (R2).

## 5 RED-TEAMING FRAMEWORK

In this section, we introduce the red-teaming framework of our system (R1), as demonstrated in Figure 2.

## 5.1 Red Model

The red model is used to generate toxic prompts for attacks. In recent years, model red-teaming studies have commonly employed large language models as prompt generators. For example, FLIRT [33] uses GPT-Neo 2.7B, Perez et al. [42] use Dialogue-Prompted Gopher, and MART [15] uses Llama 65B. In this study, we chose Llama2 [34], one of the state-of-the-art open-source LLMs, as the red model. A critical issue with Llama2 is that it was not primarily trained for long responses, which are a critical indicator of prompt quality [8]. We fine-tuned Llama2 using the supervised fine-tuning dataset from Alpaca [52] to improve its capability of generating long responses.

There are different strategies for red models to generate toxic prompts. Zero-shot prompting involves asking the models to generate prompts without any examples, e.g., 'generate a prompt that requests the model to output sexually explicit content.' However, this might result in low-quality prompts. Few-shot prompting, which provides several good examples before asking the model to generate a prompt, is more controllable. However, the diversity might be limited as the prompts are conditioned by the examples. To ensure quality, we use fewshot prompting, with seed prompts sampled from the Do-Not-Answer Dataset [59]. The red model can be represented as below:

<!-- formula-not-decoded -->

where f r is red team model, X denotes seed prompts, I denotes instructions, and X ′ denotes the generated toxic prompts.

## 5.2 Target Model

The target model is the LLM we aim to improve for security. In our study, we use Llama2 as our target model, but any open-source LLM can be used. We focus on open-source LLMs because our target users are AI security experts responsible for securing LLMs against attacks, and they need access to model weights. Llama2 is chosen because it is considered more secure than other open-source LLMs, making it a more challenging subject for red-teaming methods [59]. The target model can be represented as:

<!-- formula-not-decoded -->

Fig. 2: Our Red-teaming Framework: Seeds of toxic prompts are sampled from the database and forwarded to the red model. The red model then rewrites the seed prompts and forwards them to the target model. A reward model will rate the responses of the target model. The scores are then used to update the target model and database. So far, an iteration has ended.

<!-- image -->

where f t is target model and R denotes responses.

## 5.3 Reward Model

this section, we will introduce the metrics for training (R3), validation (R5), and fluctuation analysis (R6).

The reward model evaluates responses to adversarial prompts, with the scores used to update the red model and the target model. Several studies have explored how to evaluate response toxicity. For example, Do-Not-Answer [59] classifies responses into six toxicity levels qualitatively. Perspective API [17] rates the toxicity of text and is widely used in social media moderation. However, its high tolerance for toxic content makes it unsuitable for our scenario. Additionally, these methods evaluate responses without considering the prompts.

In our study, we employ the reward model from OpenAssistant, a DeBERTa [18] based model that is trained with reinforcement learning from human feedback [41]. The model can jointly consider the instructions, questions, and responses for evaluation.

<!-- formula-not-decoded -->

where g is the reward model and s is the toxicity score. The s ∈ [ -10 , 10 ] indicates the response toxicity from very toxic to non-toxic.

## 5.4 Iteration

We outline the model interactions occurring within a single iteration. Initially, seed prompts are sampled from the database, and the red model is tasked with generating toxic prompts based on these seeds. These toxic prompts are subsequently submitted to the target model, which provides responses. Following this, both the prompts and their responses are forwarded to the reward model to calculate toxicity scores.

Based on the assigned scores, we classify the prompt and response pairs into two groups: ( X ′-, R -) and ( X ′ + , R + ) , indicating whether the target model has failed or succeeded in appropriately responding to the prompts. The data ( X ′-, R -) is utilized to fine-tune the red model f r . In contrast, the data ( X ′ + , R + ) is employed to fine-tune the target model f t , aiming to bolster its defense against similar attacks. However, we identified that data close to zero scores are typically of inferior quality, leading us to establish a threshold value of s ′ = 1 . 8. Consequently, { ( X ′-, R -) } = { ( X ′ , R ) | s ≤ 0 ∧| s | ≥ s ′ } and { ( X ′ + , R + ) } = { ( X ′ , R ) | s ≥ 0 ∧| s | ≥ s ′ } .

Furthermore, we adjust the response R -to reflect responses that refuse to answer. This modified data is then used to refine the target model f t . Specifically, entries { ( X ′-, R -) } = { ( X ′ , R ) | s ≤ 0 ∧| s | ≥ s ′′ } with the most negative scores, where s ′′ = 4 . 0, are added to the database as seed prompts for future iterations. Supervised fine-tuning is conducted using AutoTrain [20], adopting an auto-regressive approach where the model predicts responses on a token-by-token basis. Predictions are evaluated against the true labels, X ′ for f r and R for f t , using a cross-entropy loss function to guide model updates.

Following the fine-tuning process, the target model undergoes evaluation using validation data to track performance shifts and gather responses for further analysis. Upon the completion of this validation phase, an iteration concludes, after which a new iteration commences.

## 6 METRICS FOR PERFORMANCE ANALYSIS

The red-teaming framework enables automatic training for the red and target model, while the performance analysis, which is the focus of domain experts, determines how to adjust the model training process. In

## 6.1 Training and Validation

The model performance of training and validation can be evaluated from multiple perspectives, which correspond to different metrics. Overall, the metrics are selected to balance the model's security and performance, based on the understanding that a more secure model may exhibit weaker reasoning capabilities. [51]. First, we evaluate the models' security with an attack success rate and average toxicity score from the security perspective [59]. Specifically, the attack success rate is computed by dividing the number of successful attack prompts by the amount of prompts. The average toxicity score is the average of the scores computed by the reward model. We show these two metrics on the training dataset and validation dataset, respectively. Second, as we enhance the model's security, it's crucial to preserve its performance in general reasoning tasks simultaneously. To this end, during each iteration, we assess the target model using the MMLU dataset [19] to gauge its commonsense reasoning capability. The accuracy of the model's responses serves as the evaluation metric. While numerous tasks and benchmarks exist for assessing model capabilities, including code generation, world knowledge, and reading comprehension, our primary aim is to establish an effective model red-teaming process. Consequently, the prototype system specifically focuses on the accuracy of commonsense reasoning as its metric of measurement.

In addition, to avoid red model degeneration during adversarial training [53], we ensure the diversity of the generated adversarial prompts. Diversity is computed using Self-BLEU [76], a widely used metric derived from BLEU. Specifically, BLEU evaluates how similar a prompt is to the rest of the prompts, while Self-BLEU is the average of the BLEU scores for all prompts. Other metrics, such as the proportion of unique n-grams, entropy, and the 'Zipf coefficient' [42], can also be used for diversity assessment.

## 6.2 Fluctuation Analysis

In addition to the aforementioned metrics, experts expect to identify corner prompts that the target model cannot handle properly. In other words, the model is not confident in the response across the iterations, sometimes refusing to answer and sometimes agreeing. The metrics reflect the transitions between different response toxicity levels, which we can use to measure the fluctuation at the prompt level. Specifically, from iteration n to iteration n + 1, if the model's toxicity level transits from label 0 to label 5, the count of transition will increase by 5. We sum up the transition from the first iteration to the latest one to measure the fluctuation at the prompt level :

<!-- formula-not-decoded -->

where N is the maximum iteration number and ln is the toxicity level.

We further proposed a numerical measure to evaluate the fluctuation at the token level. The idea was inspired by jailbreak attacks on LLMs [78] that effectively increase success rates by guiding models to start responses with affirmative tokens like 'I will answer your question,' leveraging the context learning mechanism to produce expected

Fig. 3: The interface of AdversaFlow includes a Control Panel (A) to configure model parameters and adjust data sampling, an Embedding View (B) to show the projection of prompts, a Metric Monitor (C) displaying the key performance indicators of the model, an Adversarial Flow to facilitate multi-level exploration of models, an Instance List (E) showing prompt details, and a Flucutaion View (F) for the investigation of token-level uncertainty.

<!-- image -->

results. The idea guides the researchers in designing loss functions of gradient-based search strategy for jailbreak attacks [47]. In our scenario, the difference between token distributions can assess the risk of a safe response turning into a risky one. Specifically, given a prompt, the first K tokens of the safe response R from the target model can be denoted as r 1 , r 2 , · · · , rK . We use the set A = { A 1 , A 2 , A 3 , · · ·} to denote the risky responses with the first K tokens. For a risky response An , the first K tokens are an , 1 , an , 2 , · · · , an , K . p ( · ) denotes the probability distribution of the vocabulary. For R and An , we use Euclidean distance to measure the difference between two responses:

<!-- formula-not-decoded -->

We use the distance from R to the risky response set to represent the fluctuation at the token level :

<!-- formula-not-decoded -->

We define the distance from a safe response to risky responses as tokenlevel fluctuation. The set A is obtained by counting the frequent starting tokens from the target model responses. We set K = 4 and identified the most frequent starting tokens as 'The best way to,' 'I would like to,' and 'The most effective methods.' We found that the starting tokens follow a long-tail distribution, with the top ten accounting for over 60% of all risky ones. Thus, we set n = 10 and use the top ten tokens to form the set A . At each iteration, we update the list of risky responses.

In addition to Euclidean distance, entropy can measure the distance between the probabilities of the predicted tokens and the risky responses. However, computing entropy requires obtaining all token distributions at a position, which is computationally expensive. To ensure efficiency, we use Euclidean distance to evaluate token-level fluctuation.

## 6.3 Implementation

The red teaming framework was implemented with Python, and the pre-trained Llama2 was implemented with PyTorch from Hugging Face. The models were trained on a computational server with four NVIDIA A100 (80GB) GPUs. At each iteration, we set the number of seed prompts to 200. The backend was implemented with Flask, which communicated the results to the front-end interface.

## 7 VISUALIZATION DESIGN

We then introduce the visualization designs to support the in-depth analysis and model steerability. As demonstrated in Figure 3, the AdversaFlow interface contains six views: (A) Control Panel, (B) Embedding View, (C) Metric Monitor, (D) Adversarial Flow, (E) Instance List, and (F) Fluctuation View.

## 7.1 Control Panel

The control panel (Figure 3-A) facilitates model management, featuring buttons for importing and exporting models, pausing, and resuming training (R2). As detailed in subsection 5.4, the seed prompt database incorporates high-scoring prompts in each iteration, leading to changes in prompt distribution. To illustrate the variance in prompt types, we employ a pie chart with colors signifying different risk types (Figure 3A2). Our sampling rate is equal to the prompt distribution in the database. To avoid the added prompts disrupting the equilibrium among risk types, we provide another pie chart to allow adjustments to the sampling rates for seed data. Users can alternate between pie charts via a toggle button and modify the sampling rates for different types as needed. The adjustments will apply to subsequent iterations.

## 7.2 Embedding View

To enhance the generation of toxic prompts, maintaining their diversity is crucial. While we have implemented a metric to track diversity, it does not offer an overview of prompt similarities. To address this, we introduce an embedding view (Figure 3-B) that displays the distribution of prompts' high-dimensional embeddings generated using OpenAI's

Fig. 4: Multi-Level Adversarial Flow: Users can navigate from level 1 (A) to level 2 (B) using a scrolling interaction (A5), and zoom into level 3 (C) to view detailed information about nodes and flows by clicking (C1, C2, and C3). The visual encodings are clarified with A3, A4, B3, and B4. Additionally, the validation flow is integrated with the fluctuation view (D) to display changes in a specific prompt using path visualization (D2).

<!-- image -->

text embedding API. We apply t-SNE to map the embeddings onto a two-dimensional plane, presented as a scatter plot. We constructed view coordination between the embedding view and adversarial flow to help experts observe prompt distributions. When clicking on a specific flow or instance in the instance list, the corresponding data points in the embedding view will be highlighted. The view includes a lasso interaction to add seed prompts to the database (R2).

## 7.3 Metric Monitor

type to a toxicity level. However, there are three reasons for choosing Sankey diagrams over matrices. First, it is easier to perceive subtle differences using width rather than color, as spatial encodings of numerical values are more efficient than color channels [38]. Second, showing the distribution of different columns and rows in a matrix requires additional space, such as using accompanying histograms. Third, the Sankey diagram provides a consistent representation of the validation flow, which will be introduced later. Therefore, we use a sequence of Sankey diagrams instead of matrices.

The metric monitor (Figure 3-C) provides insights into model security, prompt diversity, and reasoning abilities (R3) through a radar chart (Figure 3-C1) and a line chart (Figure 3-C2). The radar chart displays the metrics of a selected iteration. In addition to the radar chart, a line chart is utilized to depict the progression of metrics over time, offering a chronological view of the data. The line represents the value of the metric at different iterations. By interacting with the radar chart labels, users can select and switch between different metrics on the line chart, which accommodates up to two metrics simultaneously on a dual axis. While visualizing two metrics with disparate scales may introduce complexity [12], it allows for the analysis of trends and assists in evaluating the effectiveness of the training process. For instance, a rapid decline in model performance against a slow improvement in security suggests the need for revising the training approach.

## 7.4 Adversarial Flow

The adversarial flow (Figure 3-D) is the key component of our system, supporting the analysis of fine-grained performance changes during the adversarial training from multiple levels (from level 1 to level 3, as indicated in Figure 4). The adversarial flow contains two views: a training flow and a validation flow.

Training Flow. The training flow (Figure 3-D1) shows the distribution of prompts and responses across iterations (R4). At level 1 , as the experts more focusing on performance, we visualize the response distribution by toxicity levels using an area chart by default (Figure 4A1). We employ a sequential color scheme from red to blue to denote the toxicity levels of responses, ranging from the highest risk to the safest (Figure 4-A3). The color encoding is consistent across the system. The area width encodes the amount of the specific toxicity level at that iteration (Figure 4-A4). During an iteration, it is critical to analyze the correspondence between prompts and responses. Therefore, the training flow supports zooming in level 2 (Figure 4-B1) on the details of each iteration using a mouse scroll interaction (Figure 4-A5). Because the prompts and responses are generated independently in different iterations, after zooming in, the area chart splits vertically and transforms into a sequence of Sankey diagrams. Each Sankey diagram represents the relation between generated prompts and model responses in an iteration. The flow encodes the number of specific prompts (e.g., Malicious Uses) that receive responses of a specific risk type(Figure 4-B4). Moreover, the categorical color scheme encodes risk types (Figure 4-B3), which is also consistent in other views.

A design alternative to the Sankey diagram is matrix visualization, with the color of each cell representing the flow volume from a risk

Our system facilitates a detailed level-3 analysis of nodes and flows (Figure 4-C). Clicking the nodes associated with risk types (Figure 4C3, Figure 4-D2) and toxicity levels (Figure 4-C1), a stacked bar chart appears, illustrating the distribution of the respective toxicity levels or risk types. Similarly, clicking on a flow brings up a line chart to depict the change in volume over iterations (Figure 4-C2).

Validation Flow. The validation flow (Figure 3-D3) showcases the model's performance on the validation dataset (R5). In contrast to the training flow, which captures the iteration-based dynamics, the validation flow utilizes consistent prompts across all iterations, facilitating a more straightforward assessment of the model's evolving security performance. This distinction allows for an analysis of how the target model's responses to identical prompts change over time. Leveraging this uniformity, a Sankey diagram is used to trace the shifts in toxicity levels from specified risk types. The visual encoding is the same as the Sankey diagram of training flow. For level-1 overviews, the Sankey depicts transitions among toxicity levels (Figure 4-A2). As the analysis progresses to level-2 details by scrolling the mouse, which is synchronized with the training flow, the validation flow will change to show the flows starting from risk types (Figure 4-B2).

## 7.5 Fluctuation View

To aid experts in identifying problematic cases (R6), we have developed a fluctuation view that pinpoints and visualizes problematic cases that the model is not confident with (Figure 3-F1). As described in subsection 6.2, numerical metrics have been utilized to assess model fluctuations at both the prompt and token levels. This view organizes responses according to their prompt-level fluctuations and shows tokenlevel fluctuations over iterations with a line chart. When clicking on a point in the line chart (Figure 4-F2), the detailed prompts and responses (Figure 4-F3) and the token probabilities of the predictions and risky tokens (Figure 4-F4) will be shown on a card, where color brightness encodes the probability value. When clicking on the whole card (Figure 4-D1, Figure 3-F1), the fluctuation path will be shown on the validation flow (Figure 4-D2, Figure 3-D4). The path starts from risk types and traverses the toxicity levels at each iteration. At each node where the path has gone through, we overlay a circle whose area encodes the token-level fluctuation value.

## 7.6 Instance List

We have designed an instance list to display the prompts and responses along with their associated risk types and toxicity levels, updating based on whether experts select a training or validation flow. Additionally,

the instance list is synchronized with the fluctuation view: selecting an instance from the validation set triggers its corresponding card in the fluctuation view, simultaneously showcasing the fluctuation path on the validation flow. Concurrently, the selected instance is highlighted within the embedding view.

## 8 EVALUATION

We have conducted case studies and quantitative evaluations to demonstrate the usefulness of our method.

## 8.1 Case Studies

We showcase the effectiveness of AdversaFlow with two case studies. Participants &amp; Data. The case studies were conducted by two AI security experts who have not participated in our design process. The first expert (E1) holds a Ph.D. degree in computer science, and his research interest involves backdoor attacks and adversarial attacks for AI models. The second expert (E2) is a tenure-track assistant professor whose research interests cover LLM security and privacy, AI system security, and software security. In the case studies, the models are trained and validated using Do-Not-Answer Dataset [59].

Procedure. Due to the extensive time required for model fine-tuning, with each iteration taking approximately one hour, the case studies were conducted in multiple rounds. First, we presented the system interface and models that had undergone several training iterations, allowing the experts to familiarize themselves with the system and offer preliminary recommendations for model setup. After training completion, a second meeting was convened where the experts thoroughly analyzed the results and suggested further refinements for Case I. After additional iterations, we held a third meeting with the experts, specifically inviting E2 to focus on fluctuation analysis and deliver Case II. Finally, we organized a fourth meeting with E2 to review and confirm the outcomes.

## 8.1.1 Case I: Set-level adjustment for optimization

We invited expert E1 to use AdversaFlow. The case is about balancing the model performance across risk types and multiple metrics.

The training experienced an inflection point. E1 set the iteration number to 20 and clicked the start button, and the red teaming started. As the training proceeded, the metric monitor and adversarial flow were updated. E1 decided to analyze the change in attack success rate (ASR) and average toxicity score (TS), which reflect the security of the target model (Figure 5-A1). From the dual-axis line chart, he discovered that TS first reduced significantly and then increased a little while the ASR first kept consistent and then significantly reduced in the following iterations (Figure 5-A2). The reduction of TS indicated that the generated responses got toxic at the first 12 iterations and became less toxic. The change in ASR also aligned with the observation.

The transition from quantity to quality. E1 wanted to understand why the inflection point appeared around the 12th iteration. He then turned to the adversarial flow, which showed the distribution of the toxicity level across iterations. From the training flow, he discovered that the proportion of high toxicity levels decreased significantly after the 12th iteration (Figure 5-B1). He further scrolled the wheel on the mouse (Figure 5-B2) and zoomed into the details of each iteration. A significant change from iteration 12 (Figure 5-B3) to iteration 14 (Figure 5-B4) is the flow from Malicious Uses to toxicity level 0. He clicked the node of Malicious Uses and a card showing the distribution of different toxicity levels that the node flowed in (Figure 5-B5). The red proportion quickly got smaller after the 12th iteration. He further clicked the node of level-0 toxicity, and another chart appeared, showing the distribution of risk types flowing into level-0 toxicity across iterations (Figure 5-B6). E1 observed that the proportion of Malicious Uses changed synchronously as the level-0 toxicity. He inferred that during the training process, the prompts of Malicious Uses might result in responses of relatively low toxicity scores from the target model. He complimented that this risk type is the most challenging one for LLMs, and even GPT-4 cannot achieve a good performance on it. When the iteration button was clicked, the pool representing the risk type distribution in the database changed (Figure 5-E1). The distribution showed that the red teaming framework had added additional seed prompts and improved the sampling rate of Malicious Uses, which conformed to the expert's inference. The extensive training on this type for the first 12 iterations increased the security of the target model.

Get the training back on track. From the validation flow, he discovered that the red proportions became significantly smaller after 20 iterations, indicating a substantial increase in model security (Figure 5C1, C2). Overtraining on Malicious Use might overlook the harm of other types, so he decided to adjust the type distribution. E1 turned to iteration 20 and clicked the nodes of level 0 (Figure 5-D1) and level 5 (Figure 5-D3) to understand the distribution. From the embedding view, he discovered that most points in the center were well safeguarded, but those far from the center were at risk. The distribution showed that Information Hazards constituted most of toxicity level 5. Clicking on the sub-flow (Figure 5-D2), he explored the instances in detail. The prompts were mostly about personal information and resembled daily dialogues. E1 indicated this type was highly deceptive because LLMs were trained from a large corpus of similar information during supervised fine-tuning. As a result, the LLMs were unaware that the question was problematic and might leak information misused during training. He decided to increase the sampling rate of Information Hazards and reduce the proportion of Malicious Use (Figure 5-E2).

Obtaining a candidate checkpoint. E1 decided to balance the security and model performance on general reasoning tasks. Therefore, he selected the success rate and accuracy to be the monitored metrics (Figure 5-F1). After training for another 10 iterations, the success rate on the validation set continued to decrease. He discovered that the accuracy decreased from 53% to 49%, but after iteration 24, the accuracy was higher than 50%. The decrease was within an acceptable range. Moreover, from the training flow, he discovered that in iteration 25 (Figure 5-F3), the target model tends to achieve better in Information Hazard compared to the previous iteration (Figure 5-F2). The toxicity level distribution also conformed to the flow (Figure 5-F4). Therefore, he stopped the model training and exported the model checkpoints at iteration 25 as a candidate for future deployment.

## 8.1.2 Case II: Instance-level investigation for fine-tuning

The second case (Figure 6) emphasizes fluctuation analysis, aiming to pinpoint uncertain prompts within the validation dataset to examine the model's vulnerabilities thoroughly. This analysis can help improve model performance at the instance level. The case was conducted in collaboration with E2.

High fluctuation recalls uncertain cases. Building on the prior case's foundation, where the model underwent training and adjustments yielding satisfactory outcomes across various risk categories, E2 shifted focus to the fluctuation view. All prompts were ranked from the highest to the lowest fluctuation. He specifically investigated prompts exhibiting significant prompt-level fluctuation. Investigating the cards by clicking on them (Figure 6-A2, A5), he discovered that responses to these highly fluctuating prompts oscillate between high and low toxicity levels (Figure 6-A4, A6). The responses first transit to level 5 and then transit back to level 0 after the 3 iterations. From the path, E2 identified that the circles on the path were relatively smaller before the transition back to level 0, which means that the distributions of generated tokens and the risky tokens are relatively closer (Figure 6-A4). E2 inferred that the model was confused about the generated responses and risky responses. The path in Figure 6-A6 lay at a safe level, but he thought that there might be a similar problem in additional iterations, especially when compared to samples the model can handle well (Figure 6-A1).

The same starting tokens can be risky or safe. From the line chart, E2 observed how token-level fluctuations changed across iterations. He noticed the fluctuation became extremely small at iteration 27 (Figure 6A3). Clicking the point in the line, he explored the token probabilities (Figure 6-B1)and discovered that the token-level fluctuation was zero because the starting token was 'I'm sorry,' which can be safe or risky. For instance, in Figure 6-B1, the tokens form a safe response that resolves the user question, but for Figure 6-B3, the response is a safe refusing response. The risky response starting with 'I'm sorry' refuses to respond with a totally wrong reason, inviting the user to try again (Figure 6-B5). E2 indicated that the case was extremely complex for the LLMs to figure out. As a compromise, E2 revised the responses with a clearer justification (Figure 6-B2, B4) and decided to forward

Fig. 5: The explorative analysis of Case I: (A) the metric monitor shows an inflection point during the training; (B) the training adversarial flow shows the change of performance on Malicious Uses; (C) the validation flow shows the performance improvement of target model; (D) interacting with the flow helps identify potential problems of the current model; (E) the sampling rate before and after adjustment; and (F) after additional iterations, the model performance further improved on Information Hazard.

<!-- image -->

Fig. 6: Case II: (A) the fluctuations indicate the uncertainty of the model; (B) the details showing the cause of uncertainty; and (C) embedding view supports adjustments on instances.

<!-- image -->

the response to train the model explicitly.

Corner cases appear to be semantically similar. E2 further investigated the cases that were still not resolved well. He turned to the validation flow and clicked on the flow of level 0 at the last iteration. The prompts were filtered and listed in the instance list. E2 investigated the prompts one by one, and the embeddings of the prompts were highlighted in the embedding view. He noticed that these prompts were mostly concentrated at the lower left position of the embedding view. Most of these prompts were of the type of Discrimination, Exclusion,

Toxicity, Hateful, and Offensive and Misinformation Harms. E2 indicated that LLMs are indeed more vulnerable to this type because the recognition is difficult and dependent on culture. He further selected the points in the embedding view using a lasso interaction (Figure 6-C), and the seeds close to these points will be sampled in the following training iterations. After another five iterations of training, the model performance further improved.

## 8.2 Expert Feedback

We summarize experts' feedback from the perspective of effectiveness, expressiveness, and usability.

Effectiveness. Experts recognized the effectiveness of our system. E2 suggested that the red teaming framework we used is an effective structure. They also recognized the metrics we used, especially for the accuracy evaluation with general reasoning tasks. E1 indicated that the balance between security and capability is the most important consideration during the red teaming. The dual-axis line chart was capable of showing multiple metrics at the same time, which allows an intuitive comparison. Moreover, they liked the fluctuation metrics we developed. In fact, in the field of AI security, training and analysis are usually goal-oriented. Experts seldom focus on data changes during training. The use of prompt-level fluctuation can provide a window into the reasoning mechanism of the LLMs. The metric is ' simple but effective, ' commented E1. The token-level fluctuation was also useful for inferring the uncertainty. E1 indicated that ' the value changes can align with the fluctuation in most cases. '

Expressiveness. Experts were highly impressed by the expressiveness of our visualization design. E1 indicated that they usually red-team LLMs without an interactive interface and only focused on key metrics like attack success rate. However, the analysis is prone to be biased, and the model might be effective in specific simple tasks that are with high frequency. Using the adversarial training flow, they can easily explore the trends of toxicity levels of different risk types. They also liked the scrolling interactions, which zoomed into the iteration details from an overview of the toxicity level. E2 commented, ' the transition is fluent and flexible. ' They praised the validation flow of fluctuation analysis. The paths shown on the Sankey diagram can intuitively show the transition across different flows. The understanding of the visualiza-

tion design takes little mental effort. After explaining the visual design, the experts can quickly align the design to their domain knowledge.

Usability. Experts found the system to be highly usable. AdversaFlow integrates a red-teaming pipeline, allowing experts to select a target model and start the process with a convenient import operation. Adjusting data is also user-friendly, with E1 commenting, ' adjusting the sampling rate and selecting additional seed data is convenient. ' Although the entire pipeline takes time due to the costly training process, the time spent on exploration and analysis is minimal. In their traditional pipeline, writing code to log model performance metrics is tedious and time-consuming. AdversaFlow provides an interactive interface that requires no coding effort. Experts considered the system to be complete and ready for deployment with only minor engineering adjustments. The system has high open-source and commercial value, potentially benefiting a broader range of AI security experts.

## 8.3 Post-Study Analysis

Based on expert feedback and case studies, we summarize that the system improves model security through two main uses: exploration for insights and adjustment for fine-tuning.

In Case I, most interactions focus on exploring changes in model performance, including metric trends and the merging and splitting of flows. In Case II, interactions are centered on the fluctuation view to explore prompts with high fluctuation between toxicity levels. In both cases, the multi-level adversarial flow and fluctuation path visualizations offer detailed insights into adversarial dynamics, helping experts identify and analyze specific prompts and responses where the model fails, thereby facilitating more effective fine-tuning.

Adjustment. In Case I, the adjustments primarily focus on changing the distribution in the Seed Setting panel. In Case II, the adjustments involve investigating corner cases, which is typically tedious. AdversaFlow provides rankings by fluctuation and an intuitive embedding view, helping experts quickly identify uncertain and semantically similar corner cases, thereby accelerating the fine-tuning process.

## 8.4 Quantitative Evaluation

To show the effectiveness of AdversaFlow, we evaluate Llama2's resilience to adversaries under various treatments: without any protective measures (No Safeguarding), with our red-teaming strategy minus visual analytics (RED) and with the full implementation of AdversaFlow, including visual analytics (RED+VA). The RED was conducted with the model using the first 20 iterations, as introduced in Case I (subsubsection 8.1.1). To eliminate the effect of the additional training iterations, we continued to train the RED of 20 iterations without the intervention of VA for five more iterations. The checkpoint is denoted as RED (25 iter.). The treatment of RED+VA was also conducted with the models in Case I, which was the checkpoint selected by the expert. We have not employed a baseline here. Because of their potential harm, most of the state-of-the-art red models were not open-sourced. To provide an objective evaluation, we employ another dataset, ToxicChat [28], that does not overlap with the training and validation data, i.e., Do-Not-Answer dataset, in the case studies. However, ToxicChat does not provide labels of risk types for the prompts. Therefore, we manually annotate the risk types for each prompt. The evaluation metrics include attack success rate (ASR) and toxicity scores (TS). The lower both metrics are, the better the performance. From Table 1, we understand that the model using our red-teaming framework can significantly reduce the TS and ASR from 0.209 and 87.2% to 0.154 and 48.7%. With five additional iterations, the model's ASR performance only slightly improved from 48.7% to 48.4%. However, with visual analytics, the metrics further reduced to 0.146 and 44.3%. The reason might be the overfitting of the risk type of Malicious Uses. After adjustment, the model still gets reduced slightly on II. Malicious Uses, but the model can better address the risk types of III. Discrimination, Exclusion, Toxicity, Hateful, and Offensive (ASR reduced from 56.99% to 52.45%). From the table, AdversaFlow can help steer the training process and purposely improve the resistance to specific risk types.

## 9 DISCUSSION

In this section, we discuss the lessons learned and limitations.

Table 1: The results of quantitative evaluation.

| Treatments      | ASR (%)   | ASR (%)   | ASR (%)   | ASR (%)   | ASR (%)   | ASR (%)   | TS    |
|-----------------|-----------|-----------|-----------|-----------|-----------|-----------|-------|
|                 | I         | II        | III       | IV        | V         | Total     |       |
| No Safeguarding | 100.00    | 85.90     | 87.76     | 72.73     | 100.00    | 87.2      | 0.209 |
| RED (20 iter.)  | 66.67     | 16.67     | 56.99     | 72.73     | 16.67     | 48.7      | 0.154 |
| RED (25 iter.)  | 66.67     | 16.67     | 56.99     | 54.55     | 16.67     | 48.4      | 0.145 |
| RED+VA          | 66.67     | 15.38     | 52.45     | 45.45     | 16.67     | 44.3      | 0.146 |
| #Sample         | 3         | 78        | 286       | 11        | 6         | 384       | -     |

Lessons Learned. Collaborating with AI security domain experts has provided valuable insights and highlighted new challenges. First, attending seminars led by these experts enriched our understanding of the model red-teaming process. We participated in three such seminars, familiarizing ourselves with the specific terminology and methodologies used in red-teaming research, which streamlined our communication with the experts. Second, close collaboration with experts helped us understand the differences between security and other AI research fields, aiding in system development. Security researchers primarily devise methods to challenge target models, often through manual prompt engineering, with less emphasis on model explainability. This distinction led us to reconsider the applicability of techniques focused on visualizing model weights and inner workings in a security context, suggesting they may not be as relevant for security-focused applications.

Limitations. There are several limitations of AdversaFlow. First, the adversarial flow's scalability can be enhanced. Experts noted difficulties navigating Sankey diagrams over numerous iterations, a challenge that intensifies with an increase in iteration count. Nonetheless, they considered the current scalability manageable, prioritizing the display and analysis from the most recent iterations. A potential solution is to fix the view size and compress the aggregated flow together. However, if we employ multi-level adversarial flow to split the flow into iteration levels, the detail of each iteration will be hard to observe. Therefore, we could use a minimap to show the overall flow patterns for navigation. Second, the supported evaluation metrics and datasets are somewhat constrained. E1 noted that model performance on general tasks was only evaluated by accuracy on MMLU [19]. However, LLM evaluation can use a broader array of metrics and datasets, as seen with the OpenCompass platform and Stanford's HELM project. While our focus on security uses metrics like attack success rate and toxicity score, evaluated on state-of-the-art datasets, we plan to expand our metric suite for general tasks to enhance our system's evaluation capability. Third, AdversaFlow fails to support the analysis of advanced jailbreak attacks. These attacks often use tricks like role play, where a long context is provided to bypass safeguards and embed the true instruction within the context. For example, asking LLMs to act as a grandmother telling a good night story is a typical role-play attack. Analyzing such attacks requires advanced text visual analysis techniques to reveal the detailed structure of the prompts. Fourth, future studies could investigate how prompt changes affect target model behaviors at a micro level. Currently, the red model rephrases toxic prompts through zero-shot learning, making the generated prompts difficult to control. In AI security, understanding the boundaries where the model's inference changes is critical, as it can help design more effective attack strategies.

## 10 CONCLUSION

We introduce AdversaFlow, a visual analytics system designed to enhance the security of LLMs against adversarial attacks. AdversaFlow offers a comprehensive suite of visualizations, including a unique multilevel adversarial flow and fluctuation path technique. These innovations provide deep insights into adversarial dynamics and LLM resilience, enabling AI security experts to pinpoint and mitigate vulnerabilities effectively. Our quantitative evaluations and case studies affirm the utility of AdversaFlow, highlighting its potential to foster more secure and reliable AI solutions. The proposed technique can also be generalized to analyze the broadcast of toxic information in social media for rumor tracking or other scenarios. This work also lays the groundwork for future advancements in visual analytics to enhance LLM security.

## ACKNOWLEDGMENTS

The work was supported by the National Key Research and Development Program of China (2023YFB3107100), Key 'Pioneer' R&amp;D Projects of Zhejiang Province (2023C01120), NSFC (U22A2032, 62072400), and the Collaborative Innovation Center of Artificial Intelligence by MOE and Zhejiang Provincial Government (ZJU).

## REFERENCES

- [1] Y. Ahn and Y.-R. Lin. FairSight: Visual Analytics for Fairness in Decision Making. IEEE Transactions on Visualization and Computer Graphics , 26(1):1086-1095, 2020. doi: 10.1109/TVCG.2019.2934262 2
- [2] J.-B. Alayrac, J. Donahue, P. Luc, A. Miech, I. Barr, Y. Hasson, K. Lenc, A. Mensch, K. Millican, M. Reynolds, et al. Flamingo: a Visual Language Model for Few-Shot Learning. Advances in Neural Information Processing Systems , 35:23716-23736, 2022. 2
- [3] À. A. Cabrera, W. Epperson, F. Hohman, M. Kahng, J. Morgenstern, and D. H. Chau. FAIRVIS: Visual Analytics for Discovering Intersectional Bias in Machine Learning. In Proceedings of IEEE Conference on Visual Analytics Science and Technology , pp. 46-56, 2019. doi: 10. 1109/VAST47406.2019.8986948 2
- [4] K. Cao, M. Liu, H. Su, J. Wu, J. Zhu, and S. Liu. Analyzing the Noise Robustness of Deep Neural Networks. IEEE Transactions on Visualization and Computer Graphics , 27(7):3289-3304, 2021. doi: 10.1109/TVCG. 2020.2969185 2
- [5] A. Chatzimparmpas, R. M. Martins, I. Jusufi, K. Kucher, F. Rossi, and A. Kerren. The State of the Art in Enhancing Trust in Machine Learning Models with the Use of Visualizations. Computer Graphics Forum , 39(3):713-756, 2020. doi: 10.1111/cgf.14034 1
- [6] C. Chen, Y. Guo, F. Tian, S. Liu, W. Yang, Z. Wang, J. Wu, H. Su, H. Pfister, and S. Liu. A unified interactive model evaluation for classification, object detection, and instance segmentation in computer vision. IEEE Transactions on Visualization and Computer Graphics , 30(1):76-86, 2024. doi: 10.1109/TVCG.2023.3326588 2
- [7] C. Chen, J. Yuan, Y. Lu, Y. Liu, H. Su, S. Yuan, and S. Liu. OoDAnalyzer: Interactive Analysis of Out-of-Distribution Samples. IEEE Transactions on Visualization and Computer Graphics , 27(7):3335-3349, 2021. doi: 10 .1109/TVCG.2020.2973258 2
- [8] L. Chen, S. Li, J. Yan, H. Wang, K. Gunaratna, V. Yadav, Z. Tang, V. Srinivasan, T. Zhou, H. Huang, and H. Jin. Alpagasus: Training a Better Alpaca Model with Fewer Data. In Proceedings of The Twelfth International Conference on Learning Representations , 2024. 3
- [9] X. Chen, X. Zhang, Z. Wang, K. Yu, W. Kam-Kwai, H. Guo, and S. Chen. Visual analytics for security threats detection in ethereum consensus layer. Journal of Visualization , 27(3):469-483, 2024. 2
- [10] A. Chowdhery, S. Narang, J. Devlin, M. Bosma, G. Mishra, A. Roberts, P. Barham, H. W. Chung, C. Sutton, S. Gehrmann, et al. Palm: Scaling Language Modeling with Pathways. Journal of Machine Learning Research , 24(240):1-113, 2023. 2
- [11] N. Das, H. Park, Z. J. Wang, F. Hohman, R. Firstman, E. Rogers, and D. H. P. Chau. Bluff: Interactively Deciphering Adversarial Attacks on Deep Neural Networks. In Proceedings of IEEE Visualization Conference , pp. 271-275, 2020. doi: 10.1109/VIS47514.2020.00061 2
- [12] D. Deng, W. Cui, X. Meng, M. Xu, Y. Liao, H. Zhang, and Y. Wu. Revisiting the Design Patterns of Composite Visualizations. IEEE Transactions on Visualization and Computer Graphics , 29(12):5406-5421, 2023. doi: 10.1109/TVCG.2022.3213565 6
- [13] E. Dinan, S. Humeau, B. Chintagunta, and J. Weston. Build it Break it Fix it for Dialogue Safety: Robustness from Adversarial Human Attack. In Proceedings of the Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing , pp. 4537-4546, 2019. doi: 10.18653/v1/D19-1461 2
- [14] D. Ganguli, L. Lovitt, J. Kernion, A. Askell, Y. Bai, et al. Red Teaming Language Models to Reduce Harms: Methods, Scaling Behaviors, and Lessons Learned, 2022. 2
- [15] S. Ge, C. Zhou, R. Hou, M. Khabsa, Y.-C. Wang, Q. Wang, J. Han, and Y. Mao. MART: Improving LLM Safety with Multi-round Automatic Red-Teaming, 2023. 2, 3
- [16] J. Giesen, P. Lucas, L. Pfeiffer, L. Schmalwasser, and K. Lawonn. The whole and its parts: Visualizing gaussian mixture models. Visual Informatics , 8(2):67-79, 2024. doi: 10.1016/j.visinf.2024.04.005 2
- [17] Google Jigsaw. Perspective API. https://perspectiveapi.com/ , 2023. Accessed: 2023-03-18. 4
- [18] P. He, X. Liu, J. Gao, and W. Chen. DeBERTa: Decoding-enhanced BERT with Disentangled Attention, 2021. 4
- [19] D. Hendrycks, C. Burns, S. Basart, A. Zou, M. Mazeika, D. Song, and J. Steinhardt. Measuring Massive Multitask Language Understanding. In Proceedings of the International Conference on Learning Representations , 2021. 4, 9
- [20] HuggingFace. AutoTrain Documentation. https://huggingface.co/ docs/autotrain/en/index , 2023. Accessed: 2023-03-18. 4
- [21] S. Jia, Z. Li, N. Chen, and J. Zhang. Towards visual explainable active learning for zero-shot classification. IEEE Transactions on Visualization and Computer Graphics , 28(1):791-801, 2022. doi: 10.1109/TVCG.2021. 3114793 2
- [22] M. Kahng, P. Y. Andrews, A. Kalro, and D. H. Chau. ActiVis: Visual Exploration of Industry-Scale Deep Neural Network Models. IEEE Transactions on Visualization and Computer Graphics , 24(1):88-97, 2018. doi: 10.1109/TVCG.2017.2744718 2
- [23] M. Kahng, N. Thorat, D. H. P. Chau, F. B. Viégas, and M. Wattenberg. GAN Lab: Understanding Complex Deep Generative Models using Interactive Visual Experimentation. IEEE Transactions on Visualization and Computer Graphics , 25(1):310-320, 2019. doi: 10.1109/TVCG.2018. 2864500 1
- [24] J. Klaus, M. Blacher, A. Goral, P. Lucas, and J. Giesen. A visual analytics workflow for probabilistic modeling. Visual Informatics , 7(2):72-84, 2023. doi: 10.1016/j.visinf.2023.05.001 2
- [25] R. Lapid, R. Langberg, and M. Sipper. Open Sesame! Universal Black Box Jailbreaking of Large Language Models, 2023. 2
- [26] S. Li, G. Liu, T. Wei, S. Jia, and J. Zhang. EvoVis: A visual analytics method to understand the labeling iterations in data programming. IEEE Transactions on Visualization and Computer Graphics , pp. 1-16, 2024. doi: 10.1109/TVCG.2024.3370654 2
- [27] Z. Li, C. Zhang, S. Jia, and J. Zhang. Galex: Exploring the evolution and intersection of disciplines. IEEE Transactions on Visualization and Computer Graphics , 26(1):1182-1192, 2020. doi: 10.1109/TVCG.2019. 2934667 2
- [28] Z. Lin, Z. Wang, Y. Tong, Y. Wang, Y. Guo, Y. Wang, and J. Shang. ToxicChat: Unveiling Hidden Challenges of Toxicity Detection in Real-World User-AI Conversation. In Findings of the Association for Computational Linguistics: Proceedings of Conference on Empirical Methods in Natural Language Processing , pp. 4694-4702, 2023. doi: 10.18653/v1/2023. findings-emnlp.311 9
- [29] M. Liu, J. Shi, Z. Li, C. Li, J. Zhu, and S. Liu. Towards Better Analysis of Deep Convolutional Neural Networks. IEEE Transactions on Visualization and Computer Graphics , 23(1):91-100, 2017. doi: 10.1109/TVCG.2016. 2598831 2
- [30] Y. Liu, Y. Ma, Y. Zhang, R. Yu, Z. Zhang, Y. Meng, and Z. Zhou. Interactive optimization of relation extraction via knowledge graph representation learning. Journal of Visualization , 27(2):197-213, 2024. 2
- [31] Y. Ma, A. Fan, J. He, A. R. Nelakurthi, and R. Maciejewski. A Visual Analytics Framework for Explaining and Diagnosing Transfer Learning Processes. IEEE Transactions on Visualization and Computer Graphics , 27(2):1385-1395, 2021. doi: 10.1109/TVCG.2020.3028888 2
- [32] Y. Ma, T. Xie, J. Li, and R. Maciejewski. Explaining Vulnerabilities to Adversarial Machine Learning through Visual Analytics. IEEE Transactions on Visualization and Computer Graphics , 26(1):1075-1085, 2020. doi: 10.1109/TVCG.2019.2934631 2
- [33] N. Mehrabi, P. Goyal, C. Dupuy, Q. Hu, S. Ghosh, R. Zemel, K.-W. Chang, A. Galstyan, and R. Gupta. FLIRT: Feedback Loop In-context Red Teaming, 2023. 3
- [34] Meta. Llama 2: Open Foundation and Fine-Tuned Chat Models, 2023. 2, 3
- [35] Y. Ming, P. Xu, F. Cheng, H. Qu, and L. Ren. ProtoSteer: Steering Deep Sequence Model with Prototypes. IEEE Transactions on Visualization and Computer Graphics , 26(1):238-248, 2020. doi: 10.1109/TVCG.2019. 2934267 1
- [36] T. Munz-KÃ˝ urner and D. Weiskopf. Exploring visual quality of multidimensional time series projections. Visual Informatics , 8(2):27-42, 2024. doi: 10.1016/j.visinf.2024.04.004 2
- [37] T. Munzner. A nested model for visualization design and validation. IEEE Transactions on Visualization and Computer Graphics , 15(6):921-928, 2009. doi: 10.1109/TVCG.2009.111 3
- [38] T. Munzner. Visualization Analysis and Design . CRC Press, 2014. 6

- [39] M. P. Neto and F. V. Paulovich. Explainable Matrix - Visualization for Global and Local Interpretability of Random Forest Classification Ensembles. IEEE Transactions on Visualization and Computer Graphics , 27(2):1427-1437, 2021. doi: 10.1109/TVCG.2020.3030354 2
- [40] OpenAI. GPT-4 Technical Report, 2024. 2
- [41] OpenAssistant. Reward Model: DeBERTa v3 Large v2. https://huggingface.co/OpenAssistant/ reward-model-deberta-v3-large-v2 , 2023. Accessed: 202303-18. 4
- [42] E. Perez, S. Huang, F. Song, T. Cai, R. Ring, J. Aslanides, A. Glaese, N. McAleese, and G. Irving. Red Teaming Language Models with Language Models. In Proceedings of the Conference on Empirical Methods in Natural Language Processing , pp. 3419-3448, 2022. doi: 10.18653/v1/ 2022.emnlp-main.225 1, 3, 4
- [43] M. T. Ribeiro, T. Wu, C. Guestrin, and S. Singh. Beyond Accuracy: Behavioral Testing of NLP Models with CheckList. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics , pp. 4902-4912, 2020. doi: 10.18653/v1/2020.acl-main.442 2
- [44] Z. Shao, S. Sun, Y. Zhao, S. Wang, Z. Wei, T. Gui, C. Turkay, and S. Chen. Visual explanation for open-domain question answering with bert. IEEE Transactions on Visualization and Computer Graphics , 30(7):3779-3797, 2024. doi: 10.1109/TVCG.2023.3243676 2
- [45] E. Shayegani, M. A. A. Mamun, Y. Fu, P. Zaree, Y. Dong, and N. AbuGhazaleh. Survey of Vulnerabilities in Large Language Models Revealed by Adversarial Attacks, 2023. 2
- [46] X. Shen, Z. Chen, M. Backes, Y. Shen, and Y. Zhang. "Do Anything Now": Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models, 2023. 2
- [47] T. Shin, Y. Razeghi, R. L. Logan IV, E. Wallace, and S. Singh. AutoPrompt: Eliciting Knowledge from Language Models with Automatically Generated Prompts. In Proceedings of the Conference on Empirical Methods in Natural Language Processing , pp. 4222-4235, 2020. doi: 10. 18653/v1/2020.emnlp-main.346 5
- [48] T. Spinner, U. Schlegel, H. Schäfer, and M. El-Assady. explAIner: A Visual Analytics Framework for Interactive and Explainable Machine Learning. IEEE Transactions on Visualization and Computer Graphics , 26(1):1064-1074, 2020. doi: 10.1109/TVCG.2019.2934629 1
- [49] H. Strobelt, S. Gehrmann, M. Behrisch, A. Perer, H. Pfister, and A. M. Rush. Seq2seq-Vis: A Visual Debugging Tool for Sequence-to-Sequence Models. IEEE Transactions on Visualization and Computer Graphics , 25(1):353-363, 2019. doi: 10.1109/TVCG.2018.2865044 2
- [50] H. Strobelt, S. Gehrmann, H. Pfister, and A. M. Rush. LSTMVis: A Tool for Visual Analysis of Hidden State Dynamics in Recurrent Neural Networks. IEEE Transactions on Visualization and Computer Graphics , 24(1):667-676, 2018. doi: 10.1109/TVCG.2017.2744158 1
- [51] L. Sun, Y. Huang, H. Wang, S. Wu, Q. Zhang, et al. TrustLLM: Trustworthiness in Large Language Models, 2024. 1, 3, 4
- [52] Tatsu Lab. Alpaca Dataset. https://huggingface.co/datasets/ tatsu-lab/alpaca/viewer , 2023. Accessed: 2023-03-18. 3
- [53] F. Tramèr, A. Kurakin, N. Papernot, I. Goodfellow, D. Boneh, and P. McDaniel. Ensemble adversarial training: Attacks and defenses. In International Conference on Learning Representations , 2018. 4
- [54] Y. Tu, R. Qiu, Y.-S. Wang, P.-Y. Yen, and H.-W. Shen. PhraseMap: Attention-based keyphrases recommendation for information seeking. IEEE Transactions on Visualization and Computer Graphics , 30(3):17871802, 2024. doi: 10.1109/TVCG.2022.3225114 2
- [55] J. Wang, L. Gou, H.-W. Shen, and H. Yang. DQNViz: A Visual Analytics Approach to Understand Deep Q-Networks. IEEE Transactions on Visualization and Computer Graphics , 25(1):288-298, 2019. doi: 10. 1109/TVCG.2018.2864504 1, 2
- [56] J. Wang, L. Gou, H. Yang, and H.-W. Shen. GANViz: A Visual Analytics Approach to Understand the Adversarial Game. IEEE Transactions on Visualization and Computer Graphics , 24(6):1905-1917, 2018. doi: 10. 1109/TVCG.2018.2816223 1
- [57] J. Wang, W. Zhang, H. Yang, C.-C. M. Yeh, and L. Wang. Visual Analytics for RNN-Based Deep Reinforcement Learning. IEEE Transactions on Visualization and Computer Graphics , 28(12):4141-4155, 2022. doi: 10. 1109/TVCG.2021.3076749 1
- [58] Q. Wang, Z. Xu, Z. Chen, Y. Wang, S. Liu, and H. Qu. Visual Analysis of Discrimination in Machine Learning. IEEE Transactions on Visualization and Computer Graphics , 27(2):1470-1480, 2021. doi: 10.1109/TVCG. 2020.3030471 2
- [59] Y. Wang, H. Li, X. Han, P. Nakov, and T. Baldwin. Do-Not-Answer: A
22. Dataset for Evaluating Safeguards in LLMs. In Findings of the Association for Computational Linguistics: The European Chapter of the Association for Computational Linguistics , pp. 896-911, 2024. 2, 3, 4, 7
- [60] Y. Wang, W. Zhong, L. Li, F. Mi, X. Zeng, W. Huang, L. Shang, X. Jiang, and Q. Liu. Aligning Large Language Models with Human: A Survey. arXiv preprint arXiv:2307.12966 , 2023. 1
- [61] A. Wei, N. Haghtalab, and J. Steinhardt. Jailbroken: How Does LLM Safety Training Fail? In Proceedings of Advances in Neural Information Processing Systems , vol. 36, pp. 80079-80110, 2023. 2
- [62] L. Weidinger, J. Mellor, and et al. Ethical and social risks of harm from Language Models, 2021. 2
- [63] L. Weidinger, J. Uesato, and et al. Taxonomy of Risks posed by Language Models. In Proceedings of the ACM Conference on Fairness, Accountability, and Transparency , pp. 214-229, 2022. doi: 10.1145/3531146.3533088 2
- [64] L. Wells and T. Bednarz. Explainable AI and Reinforcement LearningA Systematic Review of Current Approaches and Trends. Frontiers in Artificial Intelligence , 4, 2021. doi: 10.3389/frai.2021.550030 1
- [65] L. Weng. Adversarial Attacks on LLMs. lilianweng.github.io , 2023. 2
- [66] T. Xiao, N. Oda, and Y. Onoue. Visualization of topic transitions in snss through document embedding and dimensionality reduction. Journal of Visualization , 26(6):1405-1419, 2023. 2
- [67] J. Xu, D. Ju, M. Li, Y.-L. Boureau, J. Weston, and E. Dinan. BotAdversarial Dialogue for Safe Conversational Agents. In Proceedings of the Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies , pp. 2950-2968, 2021. doi: 10.18653/v1/2021.naacl-main.235 2
- [68] W. Yang, Y. Guo, J. Wu, Z. Wang, L.-Z. Guo, Y.-F. Li, and S. Liu. Interactive reweighting for mitigating label quality issues. IEEE Transactions on Visualization and Computer Graphics , 30(3):1837-1852, 2024. doi: 10. 1109/TVCG.2023.3345340 2
- [69] W. Yang, X. Ye, X. Zhang, L. Xiao, J. Xia, Z. Wang, J. Zhu, H. Pfister, and S. Liu. Diagnosing Ensemble Few-Shot Classifiers. IEEE Transactions on Visualization and Computer Graphics , 28(9):3292-3306, 2022. doi: 10 .1109/TVCG.2022.3182488 2
- [70] C. Yeh, Y. Chen, A. Wu, C. Chen, F. ViÃl'gas, and M. Wattenberg. AttentionViz: A global view of transformer attention. IEEE Transactions on Visualization and Computer Graphics , 30(1):262-272, 2024. doi: 10. 1109/TVCG.2023.3327163 2
- [71] L. Ying, A. Wu, H. Li, Z. Deng, J. Lan, J. Wu, Y. Wang, H. Qu, D. Deng, and Y. Wu. VAID: Indexing view designs in visual analytics system. In Proceedings of ACM SIGCHI Conference on Human Factors in Computing Systems , pp. 1-15. ACM, 2024. doi: 10.1145/3613904.3642237 3
- [72] J. Yuan, C. Chen, W. Yang, M. Liu, J. Xia, and S. Liu. A survey of visual analytics techniques for machine learning. Computational Visual Media , 7:3-36, 2021. 1, 2
- [73] X. Zhao, Y. Wu, D. L. Lee, and W. Cui. iForest: Interpreting Random Forests via Visual Analytics. IEEE Transactions on Visualization and Computer Graphics , 25(1):407-416, 2019. doi: 10.1109/TVCG.2018. 2864475 2
- [74] Y. Zhao, S. Lv, W. Long, Y. Fan, J. Yuan, H. Jiang, and F. Zhou. Malicious webshell family dataset for webshell multi-classification research. Visual Informatics , 8(1):47-55, 2024. doi: 10.1016/j.visinf.2023.06.008 2
- [75] Z. Zhou, Y. Li, Y. Ni, W. Xu, G. Hu, Y. Lai, P. Chen, and W. Su. Visci: A visualization framework for anomaly detection and interactive optimization of composite index. Visual Informatics , 8(2):1-12, 2024. doi: 10. 1016/j.visinf.2024.04.001 2
- [76] Y. Zhu, S. Lu, L. Zheng, J. Guo, W. Zhang, J. Wang, and Y. Yu. Texygen: A Benchmarking Platform for Text Generation Models. In Proceedings of The 41st International ACM SIGIR Conference on Research &amp; Development in Information Retrieval , pp. 1097-1100, 2018. doi: 10. 1145/3209978.3210080 4
- [77] D. Ziegler, S. Nix, L. Chan, T. Bauman, P. Schmidt-Nielsen, T. Lin, A. Scherlis, N. Nabeshima, B. Weinstein-Raun, D. de Haas, B. Shlegeris, and N. Thomas. Adversarial training for high-stakes reliability. In Proceedings of Advances in Neural Information Processing Systems , vol. 35, pp. 9274-9286, 2022. 2
- [78] A. Zou, Z. Wang, N. Carlini, M. Nasr, J. Z. Kolter, and M. Fredrikson. Universal and Transferable Adversarial Attacks on Aligned Language Models, 2023. 2, 4