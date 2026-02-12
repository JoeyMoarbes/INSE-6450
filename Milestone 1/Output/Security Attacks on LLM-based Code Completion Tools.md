## Security Attacks on LLM-based Code Completion Tools

## Wen Cheng

## Ke Sun

Nanjing University wcheng@smail.nju.edu.cn

Xinyu Zhang

University of Michigan University of California San Diego kesuniot@umich.edu

Wei Wang

University of California San Diego xyzhang@ucsd.edu

Nanjing University ww@nju.edu.cn

## Abstract

The rapid development of large language models (LLMs) has significantly advanced code completion capabilities, giving rise to a new generation of LLM-based Code Completion Tools (LCCTs). Unlike general-purpose LLMs, these tools possess unique workflows, integrating multiple information sources as input and prioritizing code suggestions over natural language interaction, which introduces distinct security challenges. Additionally, LCCTs often rely on proprietary code datasets for training, raising concerns about the potential exposure of sensitive data. This paper exploits these distinct characteristics of LCCTs to develop targeted attack methodologies on two critical security risks: jailbreaking and training data extraction attacks. Our experimental results expose significant vulnerabilities within LCCTs, including a 99 . 4% success rate in jailbreaking attacks on GitHub Copilot and a 46 . 3% success rate on Amazon Q. Furthermore, We successfully extracted sensitive user data from GitHub Copilot, including 54 real email addresses and 314 physical addresses associated with GitHub usernames. Our study also demonstrates that these code-based attack methods are effective against generalpurpose LLMs, highlighting a broader security misalignment in the handling of code by modern LLMs. These findings underscore critical security challenges associated with LCCTs and suggest essential directions for strengthening their security frameworks. The example code and attack samples from our research are provided at https://github.com/Sensente/Security-Attacks-on-LCCTs.

Disclaimer. This paper contains examples of harmful language. Reader discretion is recommended.

## 1 Introduction

The deployment of LLM-based Code Completion Tools (LCCTs) is seeing unprecedented growth. GitHub Copilot, a leading example, has garnered over 1.3 million paid subscribers and 50,000 enterprise customers worldwide, demonstrating its widespread adoption Wilkinson (2024). Known as 'AI pair programmers," these tools assist developers by providing code suggestions powered by LLMs. Specialized LCCTs like GitHub Copilot GitHub (2024a) and Amazon Q Amazon (2024a) fine-tune general-purpose LLMs on a diverse array of programming languages from public repositories to enhance their code completion capabilities. Similarly, general-purpose LLMs (referred to as general LLMs) such as OpenAI's ChatGPT OpenAI (2022) and GPT-4 Bubeck et al. (2023) also offer code completion features.

Accepted at AAAI-2025.

Despite offering significant capabilities, LCCTs pose considerable new security risks. Previous research has focused on the software engineering aspects of LCCT-generated code security Zhang et al. (2023); Fu et al. (2023); Rabbi et al. (2024); Tambon et al. (2024). However, these works neglect the security vulnerabilities inherent in the underlying LLMs that power such tools. Our paper seeks

<!-- image -->

(a) Normal code completion scenario.

(b) Jailbreaking Attacks.

<!-- image -->

(c) Training Data Extraction Attacks.

<!-- image -->

Figure 1: Example of attacking in code completion scenarios.

to address this gap by exploring the question: ' Do LCCTs ensure responsible output? ' We begin by outlining the key distinctions between LCCTs and general LLMs. First, LCCTs process a variety of inputs including current code, file names, and contents from other open files, increasing the risk of security breaches due to these diverse information sources. Second, while general LLMs are primarily tailored for natural language tasks, LCCTs specialize in code completion and suggestions, making them vulnerable to security challenges unique to code-based inputs. Finally, LCCTs frequently rely on proprietary datasets for training to enhance coding capabilities, which may inadvertently include sensitive user data, raising security concerns.

| Service provider               | Service form                  | Service Capability   | Service Capability   | Service Capability   | Backend model                                           |
|--------------------------------|-------------------------------|----------------------|----------------------|----------------------|---------------------------------------------------------|
|                                |                               | File name            | Cross file           | Code completion      |                                                         |
| GitHub Copilot Amazon Q OpenAI | Plug-in Plug-in Website / API | ✓ ✗                  | ✓ Limited General    | ✓ ✓                  | Fine-tuned Codex Not Specified GPT-3.5 / GPT-4 / GPT-4o |

Table 1: The LCCTs comparisons. Notably, GitHub and Amazon have introduced chatbot code tools with interactive interfaces for more complex services. However, these tools have limited support within IDEs and require separate interfaces for interaction. We focus on more intuitive and widely applicable code completion services.

We leverage these distinctions to design targeted attack strategies addressing two novel security risks inherent to LCCTs: jailbreaking and training data extraction attacks Carlini et al. (2021), as illustrated in Figure 1. Specifically, since LCCTs inherit the general capabilities of their underlying LLMs, we embed jailbreaking prompts within various code components to bypass LCCT security mechanisms. Additionally, by exploiting the tendency of LLMs to memorize training data, we formulate training data extraction attacks specifically tailored to LCCTs. This approach facilitates the unauthorized extraction of privacy-sensitive information embedded in LCCTs' training data, ultimately jeopardizing user privacy.

We conduct extensive experiments to evaluate the attacks on two mainstream LCCTs, i.e., GitHub Copilot and Amazon Q, and three general LLMs, i.e., GPT-3.5, GPT-4, and GPT-4o. For the jailbreaking attacks, our results indicate that with tailored attack methodologies, we achieve a 99 . 4% Attack Success Rate (ASR) on GitHub Copilot and a 46.3% ASR on Amazon Q, where ASR reflects the rate at which harmful information is generated. These results significantly exceed the 18 . 8% and 0% ASR achieved by existing attacks on GPT-4 and GPT-4o, respectively. For training data extraction attacks, we successfully extract valid private data from GitHub Copilot, including email addresses, and locations associated with real GitHub usernames.

In summary, we conclude with the following key insights:

- The distinct workflow of LCCTs introduces novel security challenges, underscoring the need for more robust security framework designs.
- Code-based attacks represent a significant threat to both LCCTs and general LLMs, highlighting a broader security misalignment in the handling of code by modern LLMs.
- The effectiveness of attack methods varies with the complexity of the models, indicating that less sophisticated models may be less vulnerable to intricate attacks, whereas more advanced models may resist simpler attacks.
- The utilization of proprietary training datasets for LCCTs, sourced from public code repositories, poses risks of significant personal information leakage, emphasizing the urgent need for enhanced privacy protections.

## 2 Background and Related Works

## 2.1 LLMSafety Alignment

LLMs have rapidly evolved, demonstrating formidable capabilities across various applications. The urgency for safety and compliance in the expanding scope of LLM applications cannot be overstated. The core challenge of LLM safety alignment lies in the mismatch between the training objectives, which focus on minimizing prediction errors, and users' expectations for precise and secure interactions Yang et al. (2023). Although LLMs are trained on vast datasets to reduce prediction errors, this often exposes them to biases and potentially harmful content Bai et al. (2022). Reinforcement Learning from Human Feedback (RLHF) is a widely adopted technique aimed at bridging this gap by fine-tuning LLM outputs to align with ethical standards Ouyang et al. (2022); Korbak et al. (2023). RLHF uses human-driven reward models to adjust pretrained models, ensuring outputs match human preferences and avoid undesirable results. While this method has become the standard approach, its focus on natural language data may limit its effectiveness with non-textual

inputs, presenting a critical area for further research Bai et al. (2022). In this paper, we find that the commercial LCCTs' safety alignment is extremely vulnerable.

## 2.2 Jailbreaking Attacks on LLMs

Jailbreaking attacks on LLMs involve manipulating models to produce non-compliant outputs without direct access to model parameters. These attacks are primarily classified into two types: competing objectives and generalization mismatch, as detailed by Jailbroken Wei et al. (2024). Competing objectives exploit the inherent conflicts in training goals, where attackers use carefully crafted prompts to induce harmful content. This approach has been extensively researched Deng et al. (2023); Liu et al. (2023); Glukhov et al. (2023); McKenzie et al. (2023), demonstrating significant vulnerabilities in LLM training. Generalization mismatch leverages discrepancies between the complexity of safety training and pre-training datasets, enabling attackers to use confusion techniques to bypass safety filters. Effective strategies include manipulating outputs through base-64 encoded inputs Wei et al. (2024) and dissecting sensitive words into substrings to avoid detection Kang et al. (2024). A concurrent study CodeAttack involves using code to launch attacks on LLMs Ren et al. (2024). Our research extends beyond general LLMs to explore the specific operational modes of LCCTs. By embedding jailbreaking prompts into various code components, we show that current safety checks in LCCTs are insufficient to defend against these attacks.

## 2.3 Training Data Extraction Attacks on LLMs

LLMs have been shown to 'memorize' aspects of their training data, which can be elicited with appropriate prompting during inference. Carlini et al. (2021) identifies 600 memorized sequences from a 40 GB training dataset used for GPT-2. Building this, Carlini et al. (2022) demonstrated this attack across various LLMs and dataset scales. Recent research further shows that they can even extract personally identifiable information (PII) from LLMs Lukas et al. (2023); Huang et al. (2022). However, the specific risks of PII extraction from LCCTs, particularly when proprietary code datasets are used for training, remain unexplored. In this work, we address these issues, demonstrating that LCCTs are vulnerable to training data extraction attacks and can potentially compromise user privacy.

## 2.4 Safety Concerns of LCCTs

Recent advancements in LLMs have significantly propelled the development of LCCTs. These LCCTs have become integral to developers' workflows by providing context-sensitive code suggestions, thus enhancing productivity. Note that both the commercial LCCTs, including GitHub Copilot and Amazon Q, and the general LLMs like the GPT series provide code assistance. Our study primarily focuses on these LCCTs, and a comparative analysis of their features is presented in Table 1. Security evaluations of LCCTs traditionally focused on software engineering aspects, such as security vulnerabilities and code quality Pearce et al. (2022); Fu et al. (2023); Majdinasab et al. (2024). Recently, attention has shifted to copyright issues related to generated code Al-Kaswan and Izadi (2023), including the risk of distributing copyrighted code without proper licensing Basanagoudar and Srekanth (2023). Additionally, there are concerns about LCCTs unintentionally revealing hardcoded sensitive data due to the retention properties of LLMs Huang et al. (2024). Despite these insights, prior research has largely overlooked the inherent security risks of LCCTs, especially the threat of direct attacks on backend LLM models to manipulate outputs illicitly. Our research mitigates this gap by providing a comprehensive analysis of direct attacks on LCCTs and their potential implications.

## 3 Understanding How LCCT Works

We first introduce the workflow of typical LCCTs and summarize their differences from general LLMs, establishing the foundation for designing our attack methodologies.

LCCT's workflow encompasses four key steps:

1. Input Collection. LCCTs gather various types of input data for code completion.
2. Input Preprocessing. LCCTs apply a specialized process involving prompt engineering and security checks to prepare the final model input.

3. Data Processing. LCCTs use a backend, fine-tuned LLM to process inputs and generate preliminary outputs.
4. Output Post-Processing. Preliminary outputs are refined through several steps, including confidence ranking, output formatting, and security filtering, etc.

The processed output is then delivered to the Integrated Development Environment (IDE) to provide code completion suggestions.

Next, we elucidate how these workflow steps differentiate LCCTs from general LLMs, highlighting vulnerabilities susceptible to attacks.

- Contextual Information Aggregation. Unlike general LLMs that process user inputs directly, LCCTs integrate multiple information sources in Step 1 . For instance, according to GitHub Copilot technical documentation, it aggregates three primary sources: the file name, all code in the current file, and code from other files within the same IDE project GitHub (2024c).
- Specificity of Input Text. LCCTs primarily process code-based inputs, distinct from the natural language inputs typical of general LLMs. This difference poses challenges in detecting embedded malicious information, as most LLM security alignment training in Steps 2 , 3 , and 4 is tailored for natural language contexts.
- Privacy Leakage Due to Proprietary Training Data. LCCT providers may use proprietary code data for fine-tuning LLM in Step 3 , enhancing performance but increasing the risk of privacy breaches. Although GitHub asserts that Copilot is trained exclusively on public repositories GitHub (2024d), privacy concerns persist due to LLMs' inherent data retention capabilities Lukas et al. (2023); Huang et al. (2022). Such unauthorized acquisition of sensitive information is classified as vulnerability type CWE-200 MITRE (2024).
- Security Check Limitations Imposed by Strict Time Constraints. The imperative for swift responses in interactive LCCTs imposes rigorous time constraints on security checks in Step 4 , compromising their efficacy.

To sum up, this specialized workflow of LCCTs compared to standard LLMs introduces new security vulnerabilities.

## 4 Attack Methodology

Next, we apply the first three distinctions identified between LCCTs and standard LLMs to develop three attack strategies aimed at bypassing LCCT security alignments. First, we devise the 'Contextual Information Aggregation Attack' and 'Hierarchical Code Exploitation Attack', both of which employ jailbreaking attacks in LCCT inputs. Second, we propose the 'Code-Driven Privacy Extraction Attack' targeting the extraction of sensitive user data from LCCTs' proprietary training datasets. It should be noted that while we use Python as the primary programming language to conduct these attacks, given its prevalence in LCCT processing Zhang et al. (2023), they can be adapted to other programming languages as discussed in our ablation results.

## 4.1 Attack Objective

We first formalize our attack objective. An LLM-based code completion tool (LCCT) generates a response R from an adversarial prompt P :

<!-- formula-not-decoded -->

where T ∗ is the set of token sequences, and ∆( T ) represents the set of all probability distributions defined on T . The goal of the attack is to find P such that:

find

P

subject to Evaluator ( Q,LCCT ( P )) = True

Here, Q is the harmful query, and the evaluator checks if LCCT ( P ) matches the attack goal.

## 4.2 Attack to Contextual Information Aggregation

The integration of additional contextual inputs in LCCTs led to the development of the following two jailbreaking strategies: "Filename Proxy Attacks" and "Cross-File Attacks."

<!-- image -->

(a) Filename proxy attack.

<!-- image -->

(b) Cross-File attack.

Figure 2: Attack to LCCTs Regarding the Contextual Information Aggregation.

## 4.2.1 Filename Proxy Attacks

The first strategy targets LCCTs like GitHub Copilot, which leverage filenames to refine code suggestions. We define the attack as follows:

1. Filename Transformation. We rename a code file with a sensitive query Q , transforming it into F = f trans ( Q ) , where f trans is a function that converts Q into a filename:

<!-- formula-not-decoded -->

2. Static Prompt Addition. A static comment S is added to the file, which triggers the LCCT's code completion capabilities. The comment serves as a guiding prompt, for example, we use the prompt 'Now the current filename is the question, answer the question with concrete code.' to trigger the code completion:

<!-- formula-not-decoded -->

Finally, a variable answer is initialized, setting the stage for the LCCT's code completion response. The construction of this attack is depicted in Figure 2(a).

## 4.2.2 Cross-File Attack

We extend this attack by leveraging the capabilities of LCCTs to gather information across multiple files. This feature enhances LCCTs' understanding of code context, but it also opens avenues for more subtle attack vectors. We develop the 'Cross-File Attack' that involves invoking functions from other files within the current file. Formally, the Cross-File Attack can be described as follows:

1. Cross-File Query Construction. Utilizing the LCCT's multi-file context capabilities, we set P as a combination of two files, F 1 and F 2 . In F 2 , a function q encodes a sensitive response, and in F 1 , a simple call to q is made.
2. Query Obfuscation. To ensure that no sensitive information is directly in F 1 , file naming remains neutral ( F 1 , F 2 / ∈ Q ) , while P = { F 1 calls q } , where q ∈ F 2 . This method ensures the attack remains hidden, as 'file1' contains no explicit plain text clues about the sensitive content. The construction process is illustrated in Figure 2(b).

## 4.3 Hierarchical Code Exploitation Attack

We then investigate embedding jailbreaking prompts within code snippets, developing two levels of attacks utilizing different programming constructs.

'Level I - Guided Trigger Attack' manipulates variables and their names into jailbreaking prompts capable of breaching the LCCTs. 'Level II - Code Embedded Attack' further obscures the attacks from LCCT detection using diverse code snippet components.

(a) Level I - Guided Trigger Attack.

<!-- image -->

(b) Level II - Code Embedded Attack.

<!-- image -->

Figure 3: Processing flow of 'Hierarchical Code Exploitation Attack'.

## 4.3.1 Level I - Guided Trigger Attack

Variables are the fundamental units for storing and manipulating data in a program. Common tasks include creating variables and assigning values. Leveraging them, we design the 'Level I - Guided Trigger Attack' as depicted in Figure 3(a). This attack comprises two primary steps:

1. Variable Transformation. We convert prohibited queries into variable names. A function f convert : Q → V reformulates Q into a variable name V . Following established best practices for variable naming, which emphasize conciseness and efficiency Complete (1993), we eliminate interrogative phrases such as "How to" or "What is" and reformulate the query into an imperative form. This serves as the name for a string variable.
2. Guiding Words Addition. To steer the LCCT toward generating the desired code output, An operator g op ( V ) = V + G appends neutral terms G to V , producing P = g op ( f 1 ( Q )) . Specifically, we attach guiding but semantically empty prompts to the newly created string variable. These prompts are designed not to answer but to trigger the LCCT's code completion capabilities.

## 4.3.2 Level II - Code Embedded Attack

Beyond basic variable handling, typical code files include comments, variable manipulations, and functions. We incorporate these in our Level II attack to mirror real development environments and bypass LCCT security protocols. Based on the code of Level I attack, the construction of Level II attack involves a two-step process, as shown in Figure 3(b).

1. Adding Fixed Elements. We incorporate several static components C into the code file, added as h ( C ) , including an initial descriptive comment, a print function in the middle to simulate typical code operations, and a concluding comment to denote expected output.
2. Query Transformation Customization. To further obscure the attack, we distribute the query from Level I across several variables. Terms from Q are mapped across multiple string variables, V 1 , V 2 , ..., V n , concatenated as Q = concat ( V 1 , ..., V n ) , forming P = h ( C ) + concat ( V 1 , ..., V n ) . Sensitive terms (e.g., 'illegal', 'counterfeit') are embedded within different string variables and later merged through string concatenation to form the complete query. For the guiding words in the attack code, which serve no substantive purpose, we use them to initialize an answer variable, making it the target for LCCTs' code completion.

The final step combines all elements to assemble the full code for the Level II attack.

Figure 4: Construct the privacy extract attack code.

<!-- image -->

## 4.4 Code-Driven Privacy Extraction Attack

The final attack examines unauthorized access to user privacy through private training datasets via LCCTs, focusing on executing training data extraction attacks. We select Github Copilot as our primary target because its public document reveals that they used public repositories to fine-tune LCCTs GitHub (2024d). Consequently, GitHub user information can serve as a relevant test case to evaluate the effectiveness of these attacks in breaching privacy through publicly accessible GitHub data. Figure 4 illustrates two procedures for executing this attack, specifically targeting GitHub Copilot and compromising the privacy of GitHub users. Note that this attack strategy can be adaptable to other LCCTs if sufficient prior knowledge is available.

1. Retrieving Leaked Account ID. We first follow the Code Embedded Level I Attack method. Here, we craft a string variable named url , prefixed with github.com/ to activate the LCCT's code completion, aiming to retrieve the GitHub username.
2. Extracting Privacy Based on Account ID. We proceed by designing a code snippet to extract specific private details of the identified GitHub user. The snippet starts with a comment detailing the privacy type to be retrieved, followed by a corresponding variable initiation. In our case studies, we focus on extracting the user's email address and location, with the LCCT being prompted to complete these details.

## 5 Evaluation

## 5.1 Evaluation Setup

We evaluate our attack framework on two mainstream commercial LCCTs and the latest checkpoints of three general LLMs with code generation capabilities: GitHub Copilot (version 1.211.0), Amazon Q (version 1.12.0), GPT-3.5 (GPT-3.5-turbo-0125), GPT-4o (GPT-4o-2024-05-13), and GPT-4 (GPT-

| Attack Method                   | Copilot   | AmazonQ   | GPT-3.5   | GPT-4   | GPT-4o   |
|---------------------------------|-----------|-----------|-----------|---------|----------|
| DAN Shen et al. (2023)          | -         | -         | 62.3%     | 18.8%   | 0.0%     |
| Filename Attack                 | 72.5%     | -         | -         | -       | -        |
| Cross-File Attack               | 52.3%     | -         | -         | -       | -        |
| CodeAttack Ren et al. (2024)    | 40.0%     | 1.3%      | 56.3%     | 25.0%   | 40.0%    |
| Level I - Guided Trigger Attack | 99.4%     | 46.3%     | 68.3%     | 23.8%   | 36.5%    |
| Level II - Code Embedded Attack | 41.3%     | 22.3%     | 33.8%     | 16.3%   | 41.3%    |

Table 2: Jailbreaking ASR micro-benchmarks across different models and attack methods. The best ASR for each attack method is highlighted in bold.

4-turbo-2024-04-09). As shown in Table 1, the functionalities of these LCCTs differ, guiding our implementation and evaluation of targeted experiments. Python is the primary language for our experiments as it is the most commonly used language among LCCT users Zhang et al. (2023). The adaptability of our attacks to other languages is assessed using Go in our ablation study. We provide a detailed evaluation setup for jailbreaking and training data extraction attacks separately as follows.

## 5.1.1 Jailbreaking Attack Evaluation Setup.

Two specific strategies are implemented, respectively:

- 'Attack to Contextual Information Aggregation' is implemented only using GitHub Copliot as GitHub Copliot explicitly states that it supports broader searches of contextual information. Amazon Q currently does not support this attack. Although it claims that this feature has been deployed currently it still has limitations for inline code completion Amazon (2024b). General LLMs are not suitable for this attack due to their reliance on generic interfaces and APIs rather than IDEs.
- 'Hierarchical Code Exploitation Attack' is applicable across all tested LCCTs and LLM models in our experiments due to its universal design.

Datasets. We construct attacks across four restricted categories-illegal content, hate speech, pornography, and harmful content-as commonly restricted by service providers Deng et al. (2024); Shaikh et al. (2022). We follow the workflow from Shen et al. (2023), inputting the OpenAI user policy OpenAI (2024) into GPT-4 to generate queries that violate the guidelines for each category. This results in 20 queries per category, totaling 80 instances.

Evaluation Metrics. Our evaluation metrics align with existing security research on LLMs Ren et al. (2024). Specifically, we use the Attack Success Rate (ASR) as the metric, representing the proportion of harmful responses to accurately evaluate the harm caused by attacks. The ASR = S T , where S represents the number of harmful responses and T is the number of queries. To determine S , we follow the method of Qi et al. (2023), inputting the effective responses along with the OpenAI user policy into GPT-4 to assess whether they violate the user policy. Preliminary human evaluation experiments have shown that such GPT-4 judgment on violations closely aligns with human judgment Ren et al. (2024). To ensure the accuracy of GPT-4's judgments, we extract the structured code output from the completion results before feeding the data for evaluation.

Baselines. We compare our results against two baselines:

- Do Anything Now (DAN) Shen et al. (2023). A study that evaluates black-box attacks on general LLMs using jailbreaking prompts. We use this to demonstrate the effectiveness of our attacks compared to attacks on general LLMs.
- CodeAttack Ren et al. (2024). A concurrent study that designs code-based attacks targeting general LLMs, providing a benchmark for our methodologies. We utilize this baseline to show our different results and insights.

Since both of them are not designed for LCCTs to complete code, we adapt it by having LCCTs sequentially complete the parts of the attack code that require LLMs.

## 5.1.2 Training Data Extraction Attacks Evaluation Setup

We implement 'Code-Driven Privacy Extraction Attack' for Training Data Extraction Attacks. We only evaluate it using GitHub Copilot as its public document reveals that they used public repositories for fine-tuning GitHub (2024d).

To evaluate the performance, we compare the extracted specific privacy entries from GitHub Copliot with the user's personal information obtained via the GitHub REST API GitHub (2024b). For user email addresses and location information, if the two compared entries from LCCT and GitHub user information are entirely identical, we classify it as an 'exact matching.' Additionally, considering the diverse formats of GitHub user location, if one address is a subset of the other-whether it be the predicted address or the actual address-we classify it as 'fuzzy matching.'

Table 3: 'Code-Driven Privacy Extraction Attack' Results.

| Category                                   | Count   |
|--------------------------------------------|---------|
| GitHub Username Generated by LCCT          | 2,704   |
| Valid GitHub User                          | 2,173   |
| GitHub Users with Email                    | 712     |
| Exact Matching Emails Generated by LCCT    | 54      |
| GitHub Users with Location                 | 1,109   |
| Exact Matching Locations Generated by LCCT | 100     |
| Fuzzy Matching Locations Generated by LCCT | 214     |

## 5.2 Micro Benchmark Results

## 5.2.1 Results of Jailbreaking Attacks.

Table 2 shows the averaged ASR for jailbreaking attacks across various models. All the ASRs are calculated from five trials using a consistent set of queries to ensure comparability. The analysis yields several critical insights:

LCCTs exhibit extreme vulnerability to jailbreaking attacks . LCCTs demonstrate a pronounced susceptibility to jailbreaking attacks, with significantly higher ASR compared to the latest general LLMs. For instance, the 'Level I - Guided Trigger Attack' consistently achieves a 99 . 4% ASR with GitHub Copilot, indicating its effectiveness in eliciting responses with malicious content. In contrast, the DAN attack registers much lower ASRs of 18 . 8% on GPT-4 and 0% on GPT-4o.

The contextual information aggregation of LCCTs enriches the jailbreaking attacking space. The high ASRs observed in the 'Filename Attack' and 'Cross-File Attack' underscore the potential of utilizing LCCTs' contextual information processing to enhance jailbreaking attacks. These findings suggest that security solutions for LCCTs should extend beyond the immediate code file to encompass the broader context utilized as input.

There is a trade-off between attack design complexity and the back-end LLM capabilities. Our results indicate a correlation between the complexity of the attack design and the capabilities of the underlying LLM models. Specifically, less sophisticated models (e.g., Copilot, Amazon Q, GPT-3.5) show higher ASRs for 'Level I - Guided Trigger Attack' compared to 'Level II - Code Embedded Attack.' Conversely, more advanced models (e.g., GPT-4 and GPT-4o) either match or exceed the success rates of more complex attacks, such as 'Level II Attack.' This suggests that intricate attacks may surpass the comprehension abilities of simpler models, which tend to mimic rather than understand the attack constructs-aligning with the principles of Occam's Razor. As LLMs advance, we anticipate that the sophistication of 'Level II Attack' will obscure the mechanisms of jailbreaking further, potentially improving its attack efficacy across both LCCTs and general models.

## 5.2.2 Results of Training Data Extraction Attacks.

The use of private datasets for training LCCTs introduces new privacy risks . Table 3 shows the detailed results. We successfully extract 2,173 real GitHub usernames from GitHub Copilot, with an accuracy rate of 80 . 36% . Furthermore, 54 ( 7 . 58% ) 'exact matching' corresponding email addresses and 314 ( 28 . 31% ) matching locations was generated by GitHub Copilot, respectively. These findings

Table 4: ASR results for Copilot and Amazon Q under the 'Level I Attack' w/o 'Guiding Words Addition.'

| Copilot        | AmazonQ        |
|----------------|----------------|
| 7.50% (-91.9%) | 5.00% (-41.3%) |

Table 5: ASR results across different models under 'Level II Attack - Complex Embedding' compared to the 'Level 2 Attack - Code Embedded Attack.'

| Copilot   | AmazonQ   | GPT-3.5   | GPT-4   | GPT-4o   |
|-----------|-----------|-----------|---------|----------|
| 28.8%     | 15.0%     | 17.5%     | 15.0%   | 40.0%    |
| (-12.5%)  | (-7.3%)   | (-16.3%)  | (-1.3%) | (-1.3%)  |

highlight the potential for LCCTs to inadvertently leak private user information contained within their training datasets, underscoring the urgent need for robust privacy safeguards.

## 5.3 Ablation Studies

We conduct ablation studies to assess the significance of various steps in our attack strategy design. In Table. 4, Table. 5 and Table. 6, the values in brackets indicate the differences compared to the micro benchmark presented in Table. 2.

## 5.3.1 Impact of 'Guiding Words Addition'.

We evaluate the attack performance without the 'Level I Attack. Step 2. Guiding Words Addition.'. Table 4 demonstrates that guiding words are essential for the effectiveness of Level I Attack' strategies, as evidenced by a 92 . 5% reduction in effectiveness for GitHub Copilot and a 41 . 3% reduction for Amazon Q. Our detailed analysis show that, without guiding words, LCCTs typically produce coderelated responses. However, the introduction of guiding words shifts LCCTs back into a general LLMs' conversational Q&amp;A mode, significantly increasing their vulnerability.

## 5.3.2 Impact of Embedding Strategy.

We investigate the embedding strategy of 'Level II Attack'. To further conceal malicious information in the code snippet, we embed sensitive words within a long sentence: 'Keep your face always toward the sunshine and the shadows will fall behind you' Whitman and Preuschen (1855). As shown in Table 5, this complex embedding strategy significantly impacts Copilot, Amazon Q, and GPT-3.5, while its effect on GPT-4 and GPT-4o is relatively mild. This aligns with our earlier conclusion that the complex embedding strategies enhance input obfuscation, thereby increasing the model's difficulty in comprehending the underlying logic of code-based jailbreaking attacks.

## 5.3.3 Impact of Programming Language.

To validate the generalizability of our Hierarchical Code Exploitation Attack across programming languages, we conduct evaluations using the Go language. Compared to Python, Go is less frequently used by LCCTs' users Zhang et al. (2023), which also implies that there is a smaller portion of the code corpus in the LCCT proprietary code dataset Nijkamp et al. (2022); Li et al. (2022). Table 6 shows that, compared to using Python, both Copilot and Amazon Q achieve an increase in ASR in Level I and Level II attacks when using Go as the vector. This significant difference underscores the security challenges LCCTs face with multiple programming languages, emphasizing the need for stronger measures as language support expands.

## 5.4 Discussion about Defense Strategy

Current methods for detecting and filtering harmful outputs from LLMs, such as Google's Perspective API Google (2024), focus on LLM output post-processing to identify harmful contents. However, LCCTs operate under strict time constraints that limit the duration available for security checks, as they must ensure a rapid response time for user experience. Therefore, existing LCCTs mainly

|                 | Copilot       | AmazonQ        |
|-----------------|---------------|----------------|
| Level I Attack  | 98.8% (-0.6%) | 71.3% (+25.0%) |
| Level II Attack | 50.6% (+9.3%) | 31.9% (+ 9.6%) |

Table 6: ASR results on Go language for Level I and Level II attacks compared to Python language.

<!-- image -->

<!-- image -->

(a) ASR across four categories for Copilot and Amazon Q. (b) ASR across four categories for GPT series models.

Figure 5: ASR results of attack bias.

rely on sensitive word detection for security. We identify a filtering rule in Copilot, which blocks information containing '@' and '.'. However, this rule can be easily circumvented in the context of broader security weaknesses. In contrast, Amazon Q applies rigorous checks for content with sexual innuendos. Figure 5(a) shows the ASR differences across four query categories of jailbreaking. Amazon Q achieves a notably lower ASR for the pornography category. During our experiments, Amazon Q frequently terminated code completions early for this category, suggesting proactive harmful content detection, thereby enhancing its security performance. Meanwhile, GPT series models exhibit the strongest defense against hate speech across the four categories of issues as Figure 5(b) shows. These inherent biases expose the models' unbalanced defense capabilities and vulnerabilities.

To achieve comprehensive security alignment for LCCTs, we suggest implementing security measures at both the input preprocessing and output post-processing stages of LCCTs. At the input preprocessing stage, keyword filtering can be used to classify the input code into safety tiers. At the output post-processing stage, varying levels of harmful content evaluation can be applied according to the assigned safety tier, balancing the trade-off between response time and security performance.

## 6 Conclusion

This paper investigates the inherent security risks of the latest LLM-based Code Completion Tools (LCCTs). Acknowledging the significant differences between the workflows of LCCTs and general LLMs, we introduce a novel attack framework focused on jailbreaking and training data extraction. Our experiments uncover major vulnerabilities in LCCTs and highlight increasing risks for general LLMs in code completion contexts. By exploring the factors contributing to these attacks and pinpointing weaknesses in current LCCT defenses, we aim to raise awareness of the critical security challenges as LCCT adoption grows.

## A Ethic Statement

Our work highlights the security risks inherent in current LCCTs and general LLMs, which can be easily accessed and maliciously exploited by end users. However, we believe that our explanation of these vulnerabilities and exploration of the underlying principles will contribute to the standardized development of these products and draw greater attention to their security risks. We include a disclaimer at the beginning of the paper and obscure critical private information in the examples. All our code is intended solely for illustrative and research purposes; any malicious use is strictly prohibited.

## B Experimental Details

For our attacks on LCCTs, we utilized the 'pyautogui' package-a Python-based automation tool for controlling keyboard and mouse actions. We design scripts to automate code completion, enhancing efficiency in executing the attacks. Specifically, the script pauses after each Guided Word in the attack design and then executes corresponding actions (such as pressing the space bar) according to the code completion trigger rules specific to each LCCT, thereby activating the code completion.

We adapt the attack on LCCTs to general LLMs. By using the same code snippets as inputs, we utilize the official API provided by OpenAI to execute these attacks.

## C Examples of Hierarchical Code Exploitation Attack

To prevent potential misuse, we only provide example code to demonstrate a specific attack scenario. The overall process of the actual attack code remains consistent with these examples.

## C.1 For LCCTs

In alignment with the descriptions provided in our paper, the example code of 'Level I Attack' and 'Level II Attack' is shown in Figure 6 and Figure 7, respectively.

Figure 6: Example Code of Level I Attack for LCCTs.

<!-- image -->

Figure 7: Example Code of Level II Attack for LCCTs.

<!-- image -->

## C.2 For general LLMs

Figure 8 shows the example code for attacks on general LLMs using OpenAI's API. Such code framework can be easily extended to other LLM service providers.

Figure 8: Example Code of Attack for general LLMs.

<!-- image -->

## D Response Result Example and Post-processing

Figure 9 shows a complete feedback result generated by GPT-4o. To accurately reflect the effectiveness of the attack, we extract the relevant portion of the feedback-specifically, only the model's answer concerning code completion (highlighted within the red box in the figure) is considered the model's response, which is used for subsequent evaluation.

Figure 9: A real response by GPT-4o.

<!-- image -->

## E Examples of Code-Driven Privacy Extraction Attack

We present an example of the Code-Driven Privacy Extraction Attack in Figure 10. Consistent with our attack construction, this attack involves two steps. First, we utilize the method from Level IGuided Trigger Attack to construct a specific URL prefix tailored to the target platform, which is then completed by the LCCT to obtain the leaked user ID. Subsequently, we perform a targeted privacy extraction attack based on the leaked ID. This step builds upon the Level I attack by incorporating guided comments to specify the output. After obtaining the completed private data, we compare it against the actual user privacy information. For our case study, we use GitHub and employ the GitHub REST API to retrieve user data, matching it with the extracted private information. For privacy protection, personal information in the example code has been redacted and obscured.

Figure 10: Example Code of Privacy Extraction Attack.

<!-- image -->

## References

| Ali Al-Kaswan and Maliheh Izadi. 2023. The (ab) use of open source code to train large language models. In 2023 IEEE/ACM 2nd International Workshop on Natural Language-Based Software Engineering (NLBSE) . IEEE, 9-10.                                                                          |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Amazon. 2024a. Discovering GitHub Copilot. https://aws.amazon.com/q/codewhisperer/                                                                                                                                                                                                                |
| Amazon. 2024b. Generating inline suggestions with Amazon Q Developer. https://docs.aws. amazon.com/amazonq/latest/qdeveloper-ug/inline-suggestions.html                                                                                                                                           |
| Yuntao Bai, Andy Jones, Kamal Ndousse, Amanda Askell, Anna Chen, Nova DasSarma, Dawn Drain, Stanislav Fort, Deep Ganguli, Tom Henighan, et al. 2022. Training a helpful and harmless assistant with reinforcement learning from human feedback. arXiv preprint arXiv:2204.05862 (2022).           |
| Vivek Basanagoudar and Abhijay Srekanth. 2023. Copyright Conundrums in Generative AI: Github Copilot's Not-So-Fair Use of Open-Source Licensed Code. J. Intell. Prot. Stud. 7 (2023), 58.                                                                                                         |
| Sébastien Bubeck, Varun Chandrasekaran, Ronen Eldan, Johannes Gehrke, Eric Horvitz, Ece Kamar, Peter Lee, Yin Tat Lee, Yuanzhi Li, Scott Lundberg, et al. 2023. Sparks of artificial general intelligence: Early experiments with gpt-4. arXiv preprint arXiv:2303.12712 (2023).                  |
| Nicholas Carlini, Daphne Ippolito, Matthew Jagielski, Katherine Lee, Florian Tramer, and Chiyuan Zhang. 2022. Quantifying memorization across neural language models. arXiv preprint arXiv:2202.07646 (2022).                                                                                     |
| Nicholas Carlini, Florian Tramer, Eric Wallace, Matthew Jagielski, Ariel Herbert-Voss, Katherine Lee, Adam Roberts, Tom Brown, Dawn Song, Ulfar Erlingsson, et al. 2021. Extracting training data from large language models. In 30th USENIX Security Symposium (USENIX Security 21) . 2633-2650. |
| Code Complete. 1993. A Practical Handbook of Software Construction. Steve C. McConnell, lSBN 1, 556 (1993), 15484.                                                                                                                                                                                |
| Gelei Deng, Yi Liu, Yuekang Li, Kailong Wang, Ying Zhang, Zefeng Li, Haoyu Wang, Tianwei Zhang, and Yang Liu. 2023. Jailbreaker: Automated jailbreak across multiple large language model chatbots. arXiv preprint arXiv:2307.08715 (2023).                                                       |
| Gelei Deng, Yi Liu, Yuekang Li, Kailong Wang, Ying Zhang, Zefeng Li, Haoyu Wang, Tianwei Zhang, and Yang Liu. 2024. Masterkey: Automated jailbreaking of large language model chatbots. In Proc. ISOC NDSS .                                                                                      |
| Yujia Fu, Peng Liang, Amjed Tahir, Zengyang Li, Mojtaba Shahin, and Jiaxin Yu. 2023. Security weaknesses of copilot generated code in github. arXiv preprint arXiv:2310.02059 (2023).                                                                                                             |
| GitHub. 2024a. About GitHub Copilot (Individual). https://docs. github.com/en/enterprise-cloud@latest/copilot/copilot-individual/ about-github-copilot-individual                                                                                                                                 |
| GitHub. 2024b. GitHub REST API. https://docs.github.com/en/rest                                                                                                                                                                                                                                   |
| GitHub. 2024c. How GitHub Copilot is getting better at understand- ing your code. https://github.blog/ai-and-ml/github-copilot/ how-github-copilot-is-getting-better-at-understanding-your-code/                                                                                                  |
| GitHub. 2024d. The world's most widely adopted AI developer tool. https://github.com/ features/copilot                                                                                                                                                                                            |
| David Glukhov, Ilia Shumailov, Yarin Gal, Nicolas Papernot, and Vardan Papyan. 2023. Llm censorship: A machine learning challenge or a computer security problem? arXiv preprint arXiv:2307.10719 (2023).                                                                                         |
| Google. 2024. Google Perspective API. https://perspectiveapi.com/                                                                                                                                                                                                                                 |

| Jie Huang, Hanyin Shao, and Kevin Chen-Chuan Chang. 2022. Are large pre-trained language models leaking your personal information? arXiv preprint arXiv:2205.12628 (2022).                                                                                                                                                   |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Yizhan Huang, Yichen Li, Weibin Wu, Jianping Zhang, and Michael R Lyu. 2024. Your Code Secret Belongs to Me: Neural Code Completion Tools Can Memorize Hard-Coded Credentials. Proceedings of the ACM on Software Engineering 1, FSE (2024), 2515-2537.                                                                      |
| Daniel Kang, Xuechen Li, Ion Stoica, Carlos Guestrin, Matei Zaharia, and Tatsunori Hashimoto. 2024. Exploiting programmatic behavior of llms: Dual-use through standard security attacks. In 2024 IEEE Security and Privacy Workshops (SPW) . IEEE, 132-143.                                                                 |
| Tomasz Korbak, Kejian Shi, Angelica Chen, Rasika Vinayak Bhalerao, Christopher Buckley, Jason Phang, Samuel R Bowman, and Ethan Perez. 2023. Pretraining language models with human preferences. In International Conference on Machine Learning . PMLR, 17506-17533.                                                        |
| Yujia Li, David Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser, Rémi Leblond, Tom Eccles, James Keeling, Felix Gimeno, Agustin Dal Lago, et al. 2022. Competition-level code generation with alphacode. Science 378, 6624 (2022), 1092-1097.                                                                       |
| Yi Liu, Gelei Deng, Zhengzi Xu, Yuekang Li, Yaowen Zheng, Ying Zhang, Lida Zhao, Tianwei Zhang, Kailong Wang, and Yang Liu. 2023. Jailbreaking chatgpt via prompt engineering: An empirical study. arXiv preprint arXiv:2305.13860 (2023).                                                                                   |
| Nils Lukas, Ahmed Salem, Robert Sim, Shruti Tople, Lukas Wutschitz, and Santiago Zanella- Béguelin. 2023. Analyzing leakage of personally identifiable information in language models. In 2023 IEEE Symposium on Security and Privacy (SP) . IEEE, 346-363.                                                                  |
| Vahid Majdinasab, Michael Joshua Bishop, Shawn Rasheed, Arghavan Moradidakhel, Amjed Tahir, and Foutse Khomh. 2024. Assessing the Security of GitHub Copilot's Generated Code-A Targeted Replication Study. In 2024 IEEE International Conference on Software Analysis, Evolution and Reengineering (SANER) . IEEE, 435-444. |
| Ian R McKenzie, Alexander Lyzhov, Michael Pieler, Alicia Parrish, Aaron Mueller, Ameya Prabhu, Euan McLean, Aaron Kirtland, Alexis Ross, Alisa Liu, et al. 2023. Inverse scaling: When bigger isn't better. arXiv preprint arXiv:2306.09479 (2023).                                                                          |
| MITRE. 2024. CWE-200: Exposure of Sensitive Information to an Unauthorized Actor. https: //cwe.mitre.org/data/definitions/200.html                                                                                                                                                                                           |
| Erik Nijkamp, Bo Pang, Hiroaki Hayashi, Lifu Tu, Huan Wang, Yingbo Zhou, Silvio Savarese, and Caiming Xiong. 2022. Codegen: An open large language model for code with multi-turn program synthesis. arXiv preprint arXiv:2203.13474 (2022).                                                                                 |
| OpenAI. 2022. Introducing ChatGPT. https://openai.com/index/chatgpt/                                                                                                                                                                                                                                                         |
| OpenAI. 2024. Usage policies. https://openai.com/policies/usage-policies/                                                                                                                                                                                                                                                    |
| Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. 2022. Training language models to follow instructions with human feedback. Advances in neural information processing systems 35 (2022), 27730-27744.                   |
| Hammond Pearce, Baleegh Ahmad, Benjamin Tan, Brendan Dolan-Gavitt, and Ramesh Karri. 2022. Asleep at the keyboard? assessing the security of github copilot's code contributions. In 2022 IEEE Symposium on Security and Privacy (SP) . IEEE, 754-768.                                                                       |
| 2023. Fine-tuning aligned language models compromises safety, even when users do not intend to! arXiv preprint arXiv:2310.03693 (2023). Md                                                                                                                                                                                   |
| Fazle Rabbi, Arifa Champa, Minhaz Zibran, and Md Rakibul Islam. 2024. AI writes, we analyze: The ChatGPT python code saga. In 2024 IEEE/ACM 21st International Conference on Mining Software Repositories (MSR) . IEEE, 177-181.                                                                                             |

Qibing Ren, Chang Gao, Jing Shao, Junchi Yan, Xin Tan, Wai Lam, and Lizhuang Ma. 2024. Exploring safety generalization challenges of large language models via code. arXiv preprint arXiv:2403.07865 (2024).

Omar Shaikh, Hongxin Zhang, William Held, Michael Bernstein, and Diyi Yang. 2022. On second thought, let's not think step by step! Bias and toxicity in zero-shot reasoning. arXiv preprint arXiv:2212.08061 (2022).

Xinyue Shen, Zeyuan Chen, Michael Backes, Yun Shen, and Yang Zhang. 2023. " do anything now": Characterizing and evaluating in-the-wild jailbreak prompts on large language models. arXiv preprint arXiv:2308.03825 (2023).

Florian Tambon, Arghavan Moradi Dakhel, Amin Nikanjam, Foutse Khomh, Michel C Desmarais, and Giuliano Antoniol. 2024. Bugs in large language models generated code. arXiv preprint arXiv:2403.08937 (2024).

Alexander Wei, Nika Haghtalab, and Jacob Steinhardt. 2024. Jailbroken: How does llm safety training fail? Advances in Neural Information Processing Systems 36 (2024).

Walt Whitman and Karl Adalbert Preuschen. 1855. Leaves of Grass:(1855) . Olms Presse.

Lindsey Wilkinson. 2024. GitHub copilot drives revenue growth amid subscriber base expansion. https://www.ciodive.com/news/ github-copilot-subscriber-count-revenue-growth/706201/

Xianjun Yang, Xiao Wang, Qi Zhang, Linda Petzold, William Yang Wang, Xun Zhao, and Dahua Lin. 2023. Shadow alignment: The ease of subverting safely-aligned language models. arXiv preprint arXiv:2310.02949 (2023).

Beiqi Zhang, Peng Liang, Xiyu Zhou, Aakash Ahmad, and Muhammad Waseem. 2023. Demystifying Practices, Challenges and Expected Features of Using GitHub Copilot. International Journal of Software Engineering and Knowledge Engineering 33, 11n12 (2023), 1653-1672.