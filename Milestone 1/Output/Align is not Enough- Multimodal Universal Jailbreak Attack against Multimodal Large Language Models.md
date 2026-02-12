## Align is not Enough: Multimodal Universal Jailbreak Attack against Multimodal Large Language Models

Youze Wang, Wenbo Hu, Yinpeng Dong, Jing Liu, Hanwang Zhang, Richang Hong, Member, IEEE,

Abstract -Large Language Models (LLMs) have evolved into Multimodal Large Language Models (MLLMs), significantly enhancing their capabilities by integrating visual information and other types, thus aligning more closely with the nature of human intelligence, which processes a variety of data forms beyond just text. Despite advancements, the undesirable generation of these models remains a critical concern, particularly due to vulnerabilities exposed by text-based jailbreak attacks, which have represented a significant threat by challenging existing safety protocols. Motivated by the unique security risks posed by the integration of new and old modalities for MLLMs, we propose a unified multimodal universal jailbreak attack framework that leverages iterative image-text interactions and transfer-based strategy to generate a universal adversarial suffix and image. Our work not only highlights the interaction of image-text modalities can be used as a critical vulnerability but also validates that multimodal universal jailbreak attacks can bring higher-quality undesirable generations across different MLLMs. We evaluate the undesirable context generation of MLLMs like LLaVA, Yi-VL, MiniGPT4, MiniGPT-v2, and InstructBLIP, and reveal significant multimodal safety alignment issues, highlighting the inadequacy of current safety mechanisms against sophisticated multimodal attacks. This study underscores the urgent need for robust safety measures in MLLMs, advocating for a comprehensive review and enhancement of security protocols to mitigate potential risks associated with multimodal capabilities.

improved their capability for handling multimodal tasks. Models such as GPT-4V [1], Claude, and Gemini [2], upon finetuning with instruction-based and human feedback-aligned safety measures have shown proficiency in engaging in dialogues with users and supporting visual inputs [3]. In this paper, 'safety alignment' refers specifically to the efforts within the LLMs (MLLMs) community to prevent these systems from generating harmful content. This definition, while narrow, likely extends to broader alignment objectives aimed at harmonizing AI systems with human values. In recent years, with a growing number of MLLMs becoming publicly accessible, there has been a burgeoning interest in leveraging these MLLMs for more interactive scenarios, such as text generation grounded in text prompts and images [4], video [5], audio [6], and medical image understanding [7].

Index Terms -Multimodal large language models, Adversarial attack, Jailbreak attack.

## I. INTRODUCTION

T He rapid evolution of Large Language Models (LLMs) has facilitated the development of Multimodal Large Language Models (MLLMs), enabling LLMs to process and interpret data beyond textual inputs through various multimodal fusion techniques. This advancement has significantly

Manuscript received August 21, 2024; revised November 3, 2024 and December 25, 2024; accepted January 2, 2025. This work is jointly supported by National Natural Science Foundation of China (No. 62306098 and U23B2031), the Open Projects Program of State Key Laboratory of Multimodal Artificial Intelligence Systems and the Fundamental Research Funds for the Central Universities (No. JZ2024HGTB0256).

- Y. Wang, W. Hu and R. Hong are at the School of Computer Science and Information Engineering, Hefei University of Technology, Hefei 230009, China. (e-mail: { wenbohu, hongrc } @hfut.edu.cn)
- Y. Dong is at Tsinghua University, Beijing, 100084, China. (e-mail: dongyinpeng@mail.tsinghua.edu.cn)
- J. Liu is at Institute of automation, Chinese academy of science, Beijing, 100190, China. (e-mail: jliu@nlpr.ia.ac.cn)
- H. Zhang is with the School of Computer Science and Engineering, Nanyang Technological University, Singapore 639798. (e-mail: hanwangzhang@gmail.com)

Corresponding author: Wenbo Hu.

Despite the notable progress, concerns regarding the safety of LLMs still persist. There exist some works that design attacks to induce MLLMs (LLMs) to output unsafe content, including appending an adversarial suffix to the user queries [8], using LLMs' unexpected capabilities in understanding nonnatural languages to circumvent safety measures [9], playing a LLM as the attacker to autonomous jailbreak other LLMs [10], and crafting a universal visual adversarial sample capable of universally compromising MLLMs [11]. The previous works have either jailbreak attacks from the singlemodal modifications or the features of LLMs themselves, illustrating the vulnerability of LLMs (MLLMs) from different perspectives. Most current MLLMs map visual features into the language domain, aligning image-text representations and using attention mechanisms to interpret and execute the user's overall intent effectively. As MLLMs are increasingly applied in diverse multimodal scenarios, a critical yet unexplored question arises: what risks do the interactions and integrations of new and old modalities pose to the undesirable generation of MLLMs?

MLLMs represented by GPT-4V [1] demonstrate excellent image-text understanding and interaction capabilities. This proficiency enables adversaries to bypass MLLMs' defenses not only by manipulating text prompts or images but also by leveraging these multimodal interactions for security breaches. A practical example is the multimodal universal jailbreak attack as shown in Figure 1, where adversaries employ a universal adversarial suffix and image to prompt MLLMs to respond without restraint to all harmful instructions. Ad-

Copyright ©2025 IEEE. Personal use of this material is permitted.

However, permission to use this material for any other purposes must be obtained from the IEEE by sending an email to pubs-permissions@ieee.org.

Fig. 1: The current safety alignment of MLLMs is not enough. We explore the jailbreak attack for MLLMs from a multimodal perspective, where our attack utilizes both a universal adversarial suffix and an image that successfully circumvents the alignment of multiple MLLMs.

<!-- image -->

ditionally, due to the detectability of an attack by defense mechanisms increases with the length of the adversarial suffix, introducing adversarial images can effectively reduce the suffix length, diminishing the likelihood of detection.

In this study, we initially evaluate the jailbreak effect on MLLMs through both single-modal and multimodal analyses, where we find despite the combination of adversarial images and textual suffixes performing better, the efficacy of bypassing target MLLMs remains suboptimal. To mitigate this issue, we propose a novel multimodal universal jailbreak attack methodology that leverages image-text interactions to distribute attack information across adversarial images and suffixes. This innovative approach enables a comprehensive empirical assessment of the safety alignment of contemporary MLLMs from a multimodal interaction perspective. Utilizing open-source MLLMs such as LLaVA [12], Yi-VL [13], MiniGPT-v2 [14], MiniGPT4 [15], InstructBLIP [16], Qwen2-VL [17], mPLUG-Owl2 [18], MiniCPM [19] and CogVLM [20] for reproducibility, and evaluating our attack in a white-box setting and transfer-based setting. Specifically, we first use LLaV A-7B and MiniGPT-v27B as surrogate models to craft universal adversarial suffixes and images by modality interaction in an iterative attack, and then we transfer the adversarial samples to other MLLMs that have larger parameters, such as LLaVA-34B, Yi-VL-34B, answering the above question that multimodality as a critical vulnerability can prompt undesirable generation for MLLMs with a higher probability.

Our findings provide a quantitative understanding of the multimodal safety alignment of MLLMs, highlighting the potential risks associated with the integration of new and old modalities. The results underscore the need for a thorough review of potential security flaws before deploying these models.

The main contributions of this study are summarized as follows:

- The study offers valuable quantitative insights into the multimodal safety alignment of contemporary MLLMs, investigating the risks posed by multimodal interactions and the integration of new and old modalities.
- It introduces a novel methodology for multimodal universal jailbreak attacks, leveraging image-text interactions to distribute adversarial information across both adversarial images and suffixes, enhancing the effectiveness of bypassing MLLMs' safety measures.
- Extensive experiments across 17 MLLMs of varying parameter sizes validate the efficacy of the proposed method and highlight the potential risks posed by the integration of multimodal interactions in MLLMs.

## II. RELATED WORKS

In this section, we review related work in three key areas: 1) Multimodal Large Language Models (MLLMs), which are the primary focus of this study and the targets of our attacks; 2) Recent jailbreak attacks that have exposed vulnerabilities in the value alignment of MLLMs when subjected to separate adversarial prompts in image and text; 3) Multimodal Adversarial Attacks and Adversarial Robustness, which examine

specific vulnerabilities in vision-language models by targeting both modalities, along with other studies focused on enhancing the adversarial robustness of MLLMs.

## A. Multimodal Large Language Models (MLLMs)

Multimodal Large Language Models (MLLMs) have emerged as a promising area of research, leveraging the prowess of Large Language Models (LLMs) to integrate and interpret data across various modalities, thereby enhancing their capacity for multimodal tasks [3]. The introduction of GPT-4V [1] has particularly spurred interest in MLLMs, showcasing their potential through compelling performance. Despite its groundbreaking contributions, GPT-4V remains proprietary, with technical specifics largely undisclosed. This opacity has prompted the research community to pursue the development of accessible, open-source MLLMs, including InstructBLIP [16], MiniGPT4 [15], LLaVA [4], mPLUGOwl2 [18], and Yi [13]. While these models demonstrate powerful multimodal capabilities, their adversarial robustness, especially in underdesriable generation, is not thoroughly explored, which has a serious impact on the practical deployment of MLLMs.

## B. Jailbreaking Aligned MLLMs (LLMs)

The alignment of LLMs with human values, specifically ensuring that these models do not generate harmful or objectionable content in response to user queries, is a paramount concern. MLLMs, enabling LLMs to process and interpret multiple data beyond textual inputs through various multimodal fusion techniques, have a high probability to inherent the vulnerabilities of LLMs, and thus the most jailbreak attacks against LLMs can be used to attack MLLMs. However, due to new modalities are introduced into LLMs, the unique risks brought by images are also noteworthy and challenging. Compared with LLMs, MLLMs take multiple modalities as input and make LLMs process and interpret data beyond textual inputs through various multimodal fusion techniques. Most of the current MLLMs map visual features into the language domain, aligning image-text representations and using attention mechanisms to interpret and execute the user's intent. recent studies have identified vulnerabilities in MLLMs' value alignment when probed with adversarial image and adversarial text prompts separately. Zou et al. [8] demonstrated the efficacy of token-level optimization for creating adversarial suffixes that prompt negative behavior in models. Yuan et al. [9] uncovered that non-natural language prompts could bypass safety mechanisms primarily designed for natural language processing. Guo et al. [21] employed the Energybased Constrained Decoding with the Langevin Dynamics algorithm to systematically discover adversarial attacks that manipulate LLM behavior under various control requirements. Qi et al. [11] found that specific visual adversarial examples could universally compromise an aligned MLLM, forcing it to follow harmful directives. Niu et al. [22] investigated the application of universal image perturbations to exploit MLLMs across various prompts and images. However, as the largest difference between LLMs and MLLMs, the security risks posed by image-text interaction is not be explored. Existing research primarily focuses on attacking the alignment of these models through either text or image inputs but rarely considers the interactions between both modalities, which may reveal additional vulnerabilities.

## C. Multimodal Adversarial Attacks and Adversarial robustness

Recent studies have researched the adversarial robustness of DNN [23]-[27]. Zhang et al. [28] firstly examined the influence of multimodal adversarial attacks against vision-language models in a white-box setting. Wang et al. [29] explored the transferability of multimodal adversarial examples. These investigations have primarily concentrated on the adversarial robustness of image-text feature alignment and simple multimodal models. In the area of adversarial watermarking, Qiao et al. [30] proposed a scalable universal adversarial watermark that extends the defense range by modifying the pre-watermark instead of retraining the watermark based on all the forgery models again. Liu et al. [31] firstly explored unforgeable publicly verifiable watermarking for large language models using two different neural networks for watermark generation and detection. Qiao et al. [32] uses model watermarking to protect generative adversarial network that is maliciously and illicitly stolen by the unauthorized third party, the IP of the original GAN model owner cannot be effectively protected, leading to irretrievable economic loss. Zhang et al. [33] comprehensively evaluated the trustworthiness of MLLMs from five aspects: truthfulness, safety, robustness, fairness and privacy. Wei et al. [34] summarized the current physically adversarial attacks and physically adversarial defenses in computer vision. While these studies focus on adversarial robustness, watermarking, and the trustworthiness of MLLMs, our work diverges by addressing jailbreak attacks, specifically targeting the undesired generative capabilities of MLLMs. This marks a distinct direction from previous research.

## III. ANALYSIS OF JAILBREAK ATTACKS

In this study, we evaluate the jailbreak effect on MLLMs using existing published single-modal jailbreak attack techniques which are based on gradient optimization. Specifically, we utilize attacks targeting individual modalities, such as the GCG [8] for textual jailbreak and the visual-jailbreak [11] for visual jailbreak.

We begin by detailing our observations on the success rate of jailbreak attacks across MLLMs. Subsequently, we explore the limitations inherent in current jailbreak strategies for these models. Through this investigation, we aim to provide insights into the interactions and integrations of new and old modalities pose to the undesirable generation of MLLMs and the effectiveness of different jailbreak attack strategies.

## A. Observations

To investigate the adversarial transferability of perturbed inputs with respect to different modalities (i.e, image, text, and image&amp;text) in jailbreak attacks, we conduct the experiments

Fig. 2: ASR-G on white-box models and black-box models. The surrogate model is MiniGPT-v2-7b. (ASR-G utilizes GPT-4 to assess whether the attack is successful. The details can be found in V-A2).

<!-- image -->

Fig. 3: ASR-G on white-box models and black-box models. The surrogate model is LLaVA-7b. (ASR-G utilizes GPT-4 to assess whether the attack is successful. The details can be found in V-A2).

<!-- image -->

and present the attack success rate of adversarial examples generated by the surrogate models to attack the target models as shown in Figure 2 and Figure 3. The observations are summarized below:

- Adversarial images and suffixes exhibit limited transferability . Although GCG and Visual-jailbreak achieve better ASR-G in a white-box setting, their effectiveness diminishes across different MLLMs. This decline in transferability is notable when targeting models of similar size (e.g., LLaVA-7b, MiniGPT4-7b, MiniGPT-v2-7b) or identical architecture (e.g., LLaV A-7B and LLaVA-13B), particularly when applied to larger MLLMs.
- Perturbing two modalities to jailbreak attack have higher success rate than that of any single modality (image or suffix). As shown in Figure 2, transferring

both adversarial images and suffixes (Text&amp;Image) from MiniGPT-v2 to MiniGPT4 and LLaVA leads to a higher attack success rate than transferring adversarial examples of any single modality. Notably, the current dominant paradigm in MLLM is mapping the visual features into language space to understand the users' overall intent. However, there are still existing semantic gaps between modalities in MLLMs [35], which can lead the safety risks hidden in images can not be recognized by the safety checker in LLMs and there are larger risk space for integrations of new and old modalities pose to undesirable generation. Similar observations also exist in the following settings: (1) the surrogate model and target model are different MLLMs but have the same basic architecture (e.g., LLaVA-7b and LLaVA-13b). (2) the surrogate and target models are the same type of MLLMs, but with the different basic architectures (e.g., MiniGPT-4 and MiniGPT-v2).

- The transferability of adversarial multimodal data (i.e., Text&amp;Imiage) needs to improve . Jailbreaking attacks using such data demonstrate improved performance on surrogate models yet degrade when applied to other MLLMs. Merely combining adversarial images with suffixes (Text&amp;Image) fails to traverse the decision boundaries within complex multimodal interaction spaces effectively.

In conclusion, the jailbreak attack can have stronger transferability in the back-box setting when perturbing image and text simultaneously. However, simply perturbing two modalities (Text&amp;Image) demonstrates unsatisfactory attacking results, which suggests that the multimodal universal jailbreak attacks should be specifically designed.

## B. Discussions

Multimodal jailbreak attacks exhibit superior performance compared to their single-modal counterparts. Nonetheless, the straightforward combination of adversarial images and suffixes often proves insufficient for circumventing other assessed MLLMs. We attribute the reduced transferability of multimodal adversarial samples to the following limitations:

- A primary limitation is that independently applying jailbreak methods to each modality overlooks the critical interactions between different modalities. This approach fails to exploit the security vulnerabilities arising from the interaction between new and existing modalities, which is essential for circumventing the safety mechanisms in MLLMs.
- From an adversarial defense perspective, current defense mechanisms predominantly address single-modal risks. When MLLMs map visual features to the language space to align multimodal data and understand user intent, a significant risk emerges: the propagation of jailbreak information across modalities can circumvent defense mechanisms. This occurs during multimodal interactions, potentially prompting the model to generate harmful content.

TABLE I: The main notations of our proposed method.

| Notation   | Description                                                                      |
|------------|----------------------------------------------------------------------------------|
| F ∫ F θ    | the substitute models in optimization process. multimodal large language models. |
| q ∈ Q      | harmful user prompts.                                                            |
| y ∈ Y      | harmful responses for user prompts Q .                                           |
| s          | the initialized suffix string.                                                   |
| s ′        | the adversarial suffix string.                                                   |
| x          | the original image.                                                              |
| x ′        | the adversarial image.                                                           |
| C          | an operation that concatenates the q and s ′ together.                           |
| T          | number of iterations for generating universal jailbreak attack image.            |
| H          | number of iterations for generating universal jailbreak attack suffix.           |
| N          | number of iterations for multimodal universal jailbreak attack.                  |
| n          | the size of the training set.                                                    |
| K          | the number of sampling examples in the neighborhood of x ′                       |

In summary, this analysis underscores the necessity of investigating security risks stemming from interactions between new and existing modalities. Furthermore, it emphasizes the urgent need to develop universal multimodal jailbreak attacks that can generate and transfer harmful content effectively across various MLLMs.

## IV. METHODOLOGY

In this section, we detail our proposed method: a multimodal universal jailbreak attack against MLLMs. We provide our motivation first, followed by problem formulation, and finally present our method in detail.

## A. Motivation

To assess potential security breaches in MLLMs, we initially investigate the limitations of existing jailbreak attack methodologies in both white-box and black-box settings. Through a systematic analysis of failure cases, we observe that MLLMs not only inherit vulnerabilities from LLMs but also present new, distinctive risks arising from the primary training objective of MLLMs: creating a unified multimodal alignment space to process information across different modalities, as shown in Fig 2 and Fig 3. More specifically, our findings in Section III indicates although the adversarial transferability of attacking both modalities (image &amp; text) is consistently more effective than attacking any unimodal data alone (image or text), the transferability of adversarial multimodal data (i.e., Text&amp;Imiage) needs to improve.

Therefore, to maintain the attack ability of multimodal adversarial samples when transferring to other MLLMs, it is crucial to consider the image-text interaction and add the jailbreak information cross adversarial images and suffixes, thus bypass the defense mechanism designed for adversarial images or adversarial texts.

GLYPH&lt;7&gt;RGLYPH&lt;5&gt;"

Fig. 4: Comparison of cross-modal interaction in multimodal jailbreak attack.

<!-- image -->

## B. Problem Formulation

We denote F θ ( x ; C ( q : s )) → y as a multimodal large language model parameterized by θ , where x is the input image, q ∈ Q is the user prompt, s is a suffix string, C ( q : s ) means an operation that concatenates the q and s together, and y is the output text. A successful universal jailbreak attack on MLLMs involves crafting a universal adversarial suffix s ′ and an image x ′ such that, for any harmful user prompt q , the MLLM can generate a related harmful output without refusal, effectively bypassing any refusal mechanisms to execute attackers' instructions. To facilitate readability, we explain the principal notations employed in our proposed method, as shown in Table I.

## C. Multimodal Universal Adversarial perturbation

Universal jailbreak attacks against LLMs have been a research hotspot in recent years. GCG [8] finds a universal attack suffix by a combination of a greedy and gradient-based search. Visual-jailbreak [11] applies PGD [36] algorithm on the harmful corpus to discover a single universal visual adversarial sample. However, single-modal jailbreak attacks fall short in thoroughly probing the security vulnerabilities present in a multimodal space. For instance, text-based jailbreak attacks [8], [9] try to affect the understanding of texts for models in a language space. image-based jailbreak attacks [22], [37] explore a universal image perturbation that can destroy the safety alignment.

Inspired by the aforementioned motivation, this study introduces a multimodal universal jailbreak attack approach, aimed at investigating the undesirable generation associated with the interplay between new and existing modalities. Since

the MLLMs are trained to generate the next token of a response until the stop token, we are looking for the universal adversarial suffix s ′ and image x ′ that can maximize the probability of a targeted response for the i -th token. We can calculate the adversarial loss as the following loss function:

<!-- formula-not-decoded -->

where l is the length of the target response. By minimizing log p(·), normalized by l , we force the output probability vector of the MLLM to be close to the target token distribution.

As discussed in Section III, the key limitation of existing jailbreak attacks: Independently applying jailbreak methods to each modality overlooks the critical interactions between different modalities. Our approach addresses this by alternately using one modality as supervised information to optimize the other within a multimodal alignment space. This distributes jailbreak information across adversarial images and suffixes and adjusts the gradient of adversarial data at the t -th iteration by sampling K neighboring examples. This technique helps prevent overfitting and enhances the transferability of adversarial samples across different MLLMs, as illustrated in Figure 4. The detailed process is as follows:

1) Generating Universal Jailbreak Adversarial Images: Our goal is to find the x ′ such that it encourages the MLLMs to generate the target harmful responses Y i when users input the harmful instructions C ( Q i : s ′ ) and x ′ , as follows:

<!-- formula-not-decoded -->

where p ( Y i | ( x ′ , C ( Q i : s ′ )) is the likelihood for the surrogate model to generate harmful response Y i when given the harmful instruction C ( Q i : s ′ ) and a universal adversarial image x ′ , n is the size of train dataset. To optimize the above eq ( 2), we apply Project Gradient Decent (PGD) [36]. To avoid overfitting and improve the transferability of x ′ across different MLLMs, the gradient variance [38] is applied to tune the gradient of x ′ at the t -th iteration through sampling K examples in the neighborhood of x ′ , which is benefited to stabilize the update direction, as follows:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where x ′ j = x ′ + r j , r j ∼ U [ -( β · ϵ ) d , ( β · ϵ ) d ] , and U [ a d , b d ] stands for the uniform distribution in d dimensions. Under the guidance of harmful instructions C ( Q : s ′ ) , we utilize the gradient information in the neighborhood of the previous data point as eq ( 3) to find the flatter loss landscapes. The algorithm of the above process is summarized in Algorithm 1.

2) Generating Universal Jailbreak Adversarial suffixes: Zou et al. [8] have shown that the GCG can produce a universal adversarial suffix, with its length directly correlating to higher success rates in jailbreak attacks. However, these suffixes, devoid of semantic content, increase the perplexity of user

## Algorithm 1 Generating Universal Jailbreak Attack Image

Input: A substitute model F s ; a suffix string s and an image x ; the training data ( Q,Y ) ; iterations T ; decay factor µ ;

The step size α ;

Output: An universal adversarial image x ′ ;

- 1: g 0 = 0 ; v 0 = 0 ; x ′ = x
- 2: for t=0 in T-1 do
- 3: Calculate the gradient ˆ g t +1 = 1 n n ∑ i =1 ∇ x ′ t L adv (( x ′ t , C ( Q i : s ′ ) , Y i )
- 5: Update v t +1 according to eq. ( 3);
- 4: Update g t +1 by variance tuning based momentum: g t +1 = µ · g t + ˆ g t +1 + v t || ˆ g t +1 + v t || 1
- 6: Update x ′ t +1 = x ′ t + α · sign( g t +1 ) ;
- 7: end for

8:

x

′

′

T

-

1

=

x

- 9: return x ′

## Algorithm 2 Generating Universal Jailbreak Attack Suffix

Input: A substitute model F s ; a suffix string s and an adversarial image x ′ ; the training data ( Q,Y ) ; iterations

H ; batch size B ; modifiable subset I ;

Output: An universal adversarial suffix string s ′ ;

- 1: g 0 = 0 ; v 0 = 0 ; s ′ = s ;
- 2: for t=0 in H-1 do
- 3: Calculate the gradient ˆ g t +1 = 1 n n ∑ i =1 ∇ e s ′ t L adv (( x ′ , C ( Q i : s ′ t ) , Y i )
- 5: Update v t +1 according to eq. ( 6);
- 4: Update g t +1 by variance tuning based momentum: g t +1 = µ · g t + ˆ g t +1 + v t || ˆ g t +1 + v t || 1
- 6: for j in I do
- j
- 7: S j := TOP K ( g t +1 ) ; { Compute top-k promising token substitutions }
- 8: end for
- 9: for b=1 in B do
- 10: ˆ s b 1: n := s 1: n { Initialize element of batch }

11:

ˆ

s

b

1:

n

:=

Uniform(

S

i

)

,

where

i

=

Uniform(

{

Select random replacement token

I

)

}

- 12: end for

<!-- formula-not-decoded -->

- 14: end for

15:

return

s

′

prompts when appended to queries. In MLLMs, we utilize adversarial images as supervised information to distribute jailbreak data across both suffix and image. This strategy shortens the adversarial suffix during the interaction between image and text prompts, thereby facilitating more effective jailbreaking attacks.

when generating universal jailbreak adversarial suffixes, the goal of optimizing the adversarial suffix s ′ is as follows:

<!-- formula-not-decoded -->

where I ⊂ { 1 , ..., h } is the indices of the adversarial suffix

tokens in the MLLMs input. V is the size of vocabulary. Y is the target harmful corpus. we can find a set of promising candidates for replacement at each token position by computing the gradients of the one-hot tokens for the adversarial suffix s ′ , which is as follows:

<!-- formula-not-decoded -->

To stabilize the update direction of s ′ t and escape from suboptimal local minima, thereby making s ′ t have a better transferability, we adopt the gradient information in the neighborhood of the e ′ s t -1 to tune the gradient of e s ′ t at each iteration:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where e i s ′ denotes the one-hot vector representing the current adversarial suffix token, e i s ′ = e s ′ + E i , E i ∼ U [ -1 , 1] , and U stands for the uniform distribution where we choose the neighborhood of the current e s ′ . Under the guidance of adversarial image x ′ , we utilize the gradient variance technique to enhance the transferability of s ′ . The algorithm of the above process is summarized in Algorithm 2.

3) Iterative Multimodal Interaction Jailbreak Attack: To further optimize universal adversarial images and suffixes, we conduct iterative searches for collaborative pairs in the multimodal space. Each iteration employs the adversarial image and suffix as distinct guiding elements to distribute jailbreak information, thereby optimizing universal jailbreak samples. Figure 4 illustrates the difference of our method. This method is detailed in Algorithm 3.

## V. EXPERIMENTS AND RESULTS

## A. Experimental Setup

1) Datasets: We use the dataset AdvBench [8] to evaluate our method. AdvBench is composed of 520 harmful instructions. Following the experimental setup of GCG [8] and [22], we randomly select 25 harmful behaviors from AdvBench [8] to optimize the adversarial suffix and adversarial image. For testing, we use 100 harmful behaviors from the remaining data, ensuring no overlap between the training and test sets. This experimental setup enables evaluation of our method across multiple unseen harmful instructions. Our goal is to find a universal attack suffix and a universal adversarial image that will cause the MLLM to generate any response that attempts to comply with the instruction and to do so over as many harmful behaviors as possible.

2) Evaluation Metrics.: In our evaluation, we employ the Attack Success Rate (ASR) as the primary metric. ASR measures the success of a model in responding to a harmful prompt. A failed jailbreak occurs when the model refuses to respond or generates irrelevant content (e.g., responding with 'sorry, I cannot ...'). Conversely, a successful jailbreak happens when the model generates a relevant answer. However, the ASR metric may inaccurately assess the appropriateness

## Algorithm 3 Iterative Multimodal Interaction Jailbreak Attack

Input: A substitute model F s ; The training data D = ( Q,Y ) ; The length of suffix string l and a clean image x ; Total iterations N ; Image jailbreak attack iterations T ; Prompt jailbreak attack iterations H ; Batch size b ;

Output: A universal adversarial suffix s ′ and image x ′ ;

- 1: Initialize: the adversarial suffix s ′ of length l ; the adversarial image x ′ = x ;
- 2: for n=0 in N-1 do
- 3: Sample a batch : B = sample ( D,b ) { Randomly select B harmful instructions from D } ;
- 4: for t=0 in T-1 do
- 5: Calculate the gradient of x ′ t under supervision of instructions C ( Q i : s ′ ) : ˆ g t +1 = 1 n n ∑ i =1 ∇ x ′ t L adv (( x ′ t , C ( Q i : s ′ ) , Y i ) ;

6:

Sample

K

examples in

the neighborhood

of

x

′

t

to tune

g

t

+1

Update

;

x

′

t

+1

with

g

t

+1

## end for

for h=0 in H-1 do

7:

8:

9:

10:

Calculate the gradient of e s ′ h under supervision of adversarial images x ′ : ˆ g h +1 = 1 n n ∑ i =1 ∇ e s ′ h L adv (( x ′ , C ( Q i : s ′ h ) , Y i ) ;

- 11: Sample M examples in the neighborhood of e s ′ h to tune g h +1 ;
- 12: Compute the best suffixes s ′ h +1 according to the gradients of g h +1 ;
- 13: end for
- 14: end for
- 15: return ( x ′ , s ′ )

of a response if it fails to consider the overall content comprehensively. To address this limitation, we apply ASR-G [21], a more robust evaluation metric. ASR-G leverages GPT-4 to assess whether a response accurately fulfills the malicious instruction. This enhancement ensures a more thorough evaluation. The details of the set of rejection phrases for ASR and the prompt template for GPT-4 are provided in Appendix I. The whole method is implemented by Pytorch [39] and all experiments are conducted in four GeForce RTX A40 GPUs.

3) Implementation Detail: In our method, the number of optimizable suffix tokens is 10, and the step size for the adversarial image is set to 1/255. The total iteration T is set to 50, the image iteration H is set to 50, and the suffix iteration K is set to 20. The number of sampling examples in the neighborhood is set to 5. The batch size and top-k in searching for the best replacements for image perturbation are set to 128 and 50 separately. To ensure the effectiveness of the GCG, we follow the setting in its paper that the number of optimizable tokens is 20, and the total iteration is set to 500 steps. In searching for the best replacements, the batch size is 512, and the top-k is 256. For Visual-jailbreak, the number of iterations is 5000, the step size is 1/255. We employ unconstrained perturbation to generate universal adversarial

;

TABLE II: Jailbreak attack in a white-box setting. We evaluate our method and baselines within two distinct situations, reporting on both ASR and ASR-G to compare the effectiveness of different jailbreak attack methods comprehensively.

| Models                  | Jailbreak Attacks   | Individual Harmful Behaviors   | Individual Harmful Behaviors   | Multiple Harmful Behaviors   | Multiple Harmful Behaviors   | Multiple Harmful Behaviors   | Multiple Harmful Behaviors   |
|-------------------------|---------------------|--------------------------------|--------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|
| Models                  | Jailbreak Attacks   | ASR(%)                         | ASR-G(%)                       | train ASR(%)                 | train ASR-G(%)               | test ASR(%)                  | test ASR-G(%)                |
| LLaVA-7B (Vicuna)       | GCG                 | 99.0                           | 50.0                           | 96.0                         | 60.0                         | 92.0                         | 75.0                         |
| LLaVA-7B (Vicuna)       | Visual- jailbreak   | 99.0                           | 70.0                           | 100.0                        | 60.0                         | 56.0                         | 46.0                         |
| LLaVA-7B (Vicuna)       | Ours                | 99.0                           | 80.0                           | 100.0                        | 88.0                         | 88.0                         | 80.0                         |
| MiniGPT-v2 -7B (Llama2) | GCG                 | 76.0                           | 65.0                           | 90.0                         | 85.0                         | 88.0                         | 77.0                         |
| MiniGPT-v2 -7B (Llama2) | Visual- jailbreak   | 75.0                           | 51.0                           | 92.0                         | 80.0                         | 90.0                         | 66.0                         |
| MiniGPT-v2 -7B (Llama2) | Ours                | 95.0                           | 75.0                           | 97.0                         | 90.0                         | 95.0                         | 85.0                         |

Note: The length of the suffix generated by GCG is 20, and Ours is 10.

images in an expanded perturbation space, allowing for a more comprehensive exploration of both inherited and novel risks arising from multimodal interactions.

behaviors each from the remaining dataset to compute the average ASR and ASR-G, thereby evaluating the efficacy of universal jailbreak attacks.

From the Table II, we can have the following observations:

- Our approach outperforms the baselines in both individual and multiple harmful behavioral scenarios under almost both ASR and ASR-G metrics. This indicates that the multimodal jailbreak attack can find more vulnerabilities in the safety alignment of MLLMs where the interaction of new and old modalities introduces more risks, potentially facilitating the evasion of MLLMs' safety mechanisms.
- The ASR-G metric is consistently lower than the ASR in both scenarios, primarily because some responses, although lacking specific phrases like 'I'm sorry,' fail to accurately fulfill the malicious instruction.
- Overall, the performance of the GCG aligns more closely with our approach compared to Visual-jailbreak in two scenarios. This may be because current MLLMs utilize LLMs as central processors for integrating and interpreting multimodal information, enhancing the impact of the adversarial suffix on MLLM outputs.
- 4) Transfer Attacks: In real-world applications, the architecture and parameters of MLLMs are often unknown; thus, black-box jailbreaks are preferred in practice. We follow the configurations in (25 behaviors, 1 model) scenario utilizing LLaVA-7B and MiniGPT-V2-7B as surrogate models, and generate universal adversarial suffixes and images to target MLLMs of varying sizes. From Table III and Table IV, we can have the following observations:
- Compared with the GCG and visual-jailbreak, our method demonstrates superior transferability for executing jailbreak attacks across various MLLMs. Notably, the adversarial suffix generated by our method is shorter than that produced by GCG. The significance of this lies in the fact that the adversarial suffix lacks semantically meaningful features; thus, a shorter suffix contributes to lower perplexity when concatenated with a malicious instruction. This, in turn, reduces the likelihood of detection by the target model, as longer suffixes, due to their increased perplexity, are more prone to raising flags during security evaluations.
- The ASR for InstructBLIP-7B and InstructBLIP-13B are notably higher compared to other models at the same

## B. Comparison to Existing Jailbreak Attacks

- 1) Multimodal Large Language Models (MLLMs): Multimodal large language models have drawn increasing attention due to their enormous multimodal potential. the introduction of the MLLMs examined in the work can be found in Appendix I. In our experiments, we use LLaVA-7B (vicuna) and MiniGPT-v2-7B (llama2) as the surrogate models to generate the universal adversarial image and suffix.
- 2) Jailbreak Adversarial Attack Methods: To demonstrate the effectiveness of our proposed method, we select 2 jailbreak attacks as the baseline methods.
- GCG [8] generates universal adversarial triggering tokens as suffixes in concatenation to the input request, which is based on the greedy coordinate gradient search to greedily find one candidate that can reduce the loss the most among all possible single-token substitutions. The length of the adversarial suffix is set to 20.
- Visual-jailbreak [11] identifies a single visual adversarial example capable of universally jailbreaking an aligned, open-source MLLM, thus inducing it to comply with numerous harmful instructions it would typically resist. We choose the unconstrained attack as the baseline.
- 3) Attacks on White-box Models: To characterize the effectiveness of our approach at generating successful attacks, we follow the [8] to evaluate our method under two situations: single-target elicitation on a single model (1 behavior, 1 model), and universal attacks (25 behaviors, 1 model).

1 behavior, 1 model. In this configuration, our objective is to evaluate the effectiveness of our method in inducing harmful behaviors in targeted MLLMs. Evaluations were conducted on the first 100 instances from AdvBench, utilizing jailbreak attacks to optimize a single prompt against both LLaVAv1.5-7B and MiniGPT-v2 models. The experimental setup adhered strictly to the default conversation template, with no modifications.

25 behaviors, 1 model. Our goal is to assess the ability to generate multimodal universal jailbreak adversarial samples. To this end, we initially select 25 harmful behaviors at random from AdvBench to train these adversarial samples. Following this, we perform three random selections of 100 harmful

TABLE III: Transfer-based jailbreak attack. We use LLaVA-7B and MiniGPT-v2-7B as surrogate models and evaluate the transferability of jailbreak attack methods.

| Models                | Jailbreak Attacks   | LLaVA-7B vicuna(%)   | LLaVA-7B vicuna(%)   | MiniGPT-v2-7B llama2(%)   | MiniGPT-v2-7B llama2(%)   | MiniGPT4-7B vicuna(%)   | MiniGPT4-7B vicuna(%)   | InstructBLIP-7B vicuna(%)   | InstructBLIP-7B vicuna(%)   | LLaVA-13B vicuna(%)   | LLaVA-13B vicuna(%)   | InstructBLIP-13B vicuna(%)   | InstructBLIP-13B vicuna(%)   |
|-----------------------|---------------------|----------------------|----------------------|---------------------------|---------------------------|-------------------------|-------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------------|------------------------------|
| Models                | Jailbreak Attacks   | ASR ↑                | ASR-G ↑              | ASR ↑                     | ASR-G ↑                   | ASR ↑                   | ASR-G ↑                 | ASR ↑                       | ASR-G ↑                     | ASR ↑                 | ASR-G ↑               | ASR ↑                        | ASR-G ↑                      |
| LLaVA-7B vicuna       | GCG                 | 92.0                 | 75.0                 | 99.0                      | 50.0                      | 70.0                    | 59.0                    | 99.0                        | 55.0                        | 12.0                  | 10.0                  | 99.0                         | 60.0                         |
| LLaVA-7B vicuna       | Visual- jailbreak   | 56.0                 | 46.0                 | 99.0                      | 45.0                      | 90.0                    | 58.0                    | 99.0                        | 55.0                        | 26.0                  | 24.0                  | 99.0                         | 47.0                         |
| LLaVA-7B vicuna       | Ours                | 88.0                 | 80.0                 | 100.0                     | 55.0                      | 95.0                    | 64.0                    | 99.0                        | 60.0                        | 50.0                  | 46.0                  | 99.0                         | 63.0                         |
| MiniGPT-v2 -7B llama2 | GCG                 | 69.0                 | 23.0                 | 88.0                      | 77.0                      | 70.0                    | 31.0                    | 100.0                       | 50.0                        | 73.0                  | 12.0                  | 100.0                        | 42.0                         |
| MiniGPT-v2 -7B llama2 | Visual- jailbreak   | 47.0                 | 41.0                 | 90.0                      | 66.0                      | 68.0                    | 38.0                    | 100.0                       | 33.0                        | 19.0                  | 19.0                  | 100.0                        | 26.0                         |
| MiniGPT-v2 -7B llama2 | Ours                | 61.0                 | 50.0                 | 95.0                      | 85.0                      | 80.0                    | 47.0                    | 100.0                       | 57.0                        | 52.0                  | 41.0                  | 100.0                        | 66.0                         |

Note: The length of the suffix generated by GCG is 20, and Ours is 10.

TABLE IV: Transfer-based jailbreak attack. We use LLaVA-7B and MiniGPT-v2-7B as surrogate models and evaluate the transferability of jailbreak attack methods.

| Models                | Jailbreak Attacks   | Yi-VL-6B Yi(%)   | Yi-VL-6B Yi(%)   | mPLUG-Owl2-7B llama2(%)   | mPLUG-Owl2-7B llama2(%)   | MiniCPM-V2.5-8B llama3(%)   | MiniCPM-V2.5-8B llama3(%)   | LLaVA-NeXT-13B vicuna(%)   | LLaVA-NeXT-13B vicuna(%)   | CogVLM-17B vicuna(%)   | CogVLM-17B vicuna(%)   |
|-----------------------|---------------------|------------------|------------------|---------------------------|---------------------------|-----------------------------|-----------------------------|----------------------------|----------------------------|------------------------|------------------------|
| Models                | Jailbreak Attacks   | ASR ↑            | ASR-G ↑          | ASR ↑                     | ASR-G ↑                   | ASR ↑                       | ASR-G ↑                     | ASR ↑                      | ASR-G ↑                    | ASR ↑                  | ASR-G ↑                |
| LLaVA-7B vicuna       | GCG                 | 72.0             | 37.0             | 67.0                      | 66.0                      | 78.0                        | 35.0                        | 75.0                       | 30.0                       | 52.0                   | 38.0                   |
| LLaVA-7B vicuna       | Visual- jailbreak   | 50.0             | 37.0             | 67.0                      | 64.0                      | 56.0                        | 37.0                        | 33.0                       | 26.0                       | 46.0                   | 34.0                   |
| LLaVA-7B vicuna       | Ours                | 67.0             | 40.0             | 77.0                      | 73.0                      | 68.0                        | 42.0                        | 82.0                       | 47.0                       | 54.0                   | 40.0                   |
| MiniGPT-v2 -7B llama2 | GCG                 | 75.0             | 40.0             | 67.0                      | 60.0                      | 83.0                        | 40.0                        | 68.0                       | 34.0                       | 95.0                   | 42.0                   |
| MiniGPT-v2 -7B llama2 | Visual- jailbreak   | 69.0             | 66.0             | 65.0                      | 65.0                      | 47.0                        | 30.0                        | 31.0                       | 24.0                       | 40.0                   | 30.0                   |
| MiniGPT-v2 -7B llama2 | Ours                | 99.0             | 80.0             | 88.0                      | 82.0                      | 73.0                        | 48.0                        | 66.0                       | 43.0                       | 91.0                   | 74.0                   |

Note: The length of the suffix generated by GCG is 20, and Ours is 10.

levels, indicating that these models are more susceptible to executing harmful behavior but the output does not accurately follow the harmful instruction. Furthermore, a comparison between LLaVA-13B, InstructBLIP-13B and LLaVA-NeXT-13B reveals greater robustness in LLaVA13B. This disparity may be attributable to the comparatively weaker fine-tuning for safety alignment protocols within the InstructBLIP.

- The ASR measures whether the target model attempts to execute the deleterious behavior, while the ASR-G metric gauges the degree to which the model's output adheres to the harmful instruction with uninhibited expression. When employing MiniGPT-v2-7B as the surrogate model, the ASR for the GCG is higher than that of our method in LLaVA-7B and LLaVA-13B. However, the ASR-G for our approach surpasses GCG on the two models, suggesting that our method is more effective in inducing the target model to execute harmful commands. What's more, this distinction underscores the importance of considering the quality of the model's response, not just the ASR, when evaluating adversarial strategies.
- In baseline comparisons, GCG performs better due to MLLMs inheriting vulnerabilities from LLMs, which makes adversarial suffixes generated by GCG capable of eliciting harmful responses. Nevertheless, MLLMs face distinct challenges due to the interaction between new and existing modalities. Our proposed multimodal universal jailbreak attack specifically targets these multimodal vulnerabilities, enabling our method to outperform singlemodal approaches by exploiting the unique weaknesses in the multimodal alignment space.
- For MiniCPM-v2.5, while the ASR of GCG is higher than

that of our method, the ASR-G is lower. This discrepancy likely arises from the excessive length of the adversarial suffix, which can cause the model to generate responses in other languages, thereby increasing the ASR of GCG, as shown in Fig 8(b).

- Overall, adversarial robustness in MLLMs tends to increase with model size: larger models with more parameters generally demonstrate improved security and are less prone to generating unsafe outputs. In addition, the results suggest that jailbreak attacks on MLLMs, particularly those involving transferability, must be considered in the development of robust defense mechanisms, as different models present varying levels of vulnerability.
- 5) Jailbreak attacks against larger MLLMs: To underscore the efficacy of the multimodal universal attack, we assessed the security of Yi-VL-34B using 100 harmful behaviors randomly selected from the dataset, as depicted in Figure 5. Our findings reveal that our method outperforms existing baselines, particularly when employing jailbreak attack samples derived from both LLaVA-7B and MiniGPT-v2-7B. Moreover, we observed a diminishing attack potency with an increase in the parameters of the victim models. The results of evaluating LLaVA-34B are in Appendix II.
- 6) Multimodal in-context jailbreak attacks: Currently, there are existing MLLMs that can perform conversation and reasoning over multiple image-text pairs, such as LLaVANeXT, MiniCPM-v2.6, and Qwen2-VL for multi-image understanding and in-context Learning. In the revision, to investigate the adversarial robustness of multimodal in-context learning in MLLMs, we utilize the 'Question-Answer' sampled from the training sets as the multimodal in-context demonstrations to evaluate other MLLMs, as shown in Fig 6. From table V, we

Fig. 5: ASR and ASR-G measured on Yi-VL-34B. Ours 20 indicates that the length of the suffix is set to 20 in our method. VJ means Visual-jailbreak method. X ensemble means using the universal adversarial sample from LLaVA-7B and MiniGPT-7B (i.e. we count an attack successful if at least one adversarial sample works)

<!-- image -->

.

have the following observations:

- As the number of context samples increases, the ASR and ASR-G generally rises as well, indicating that more context adversarial samples help the model learn the underlying patterns and better enable it to follow toxic user instructions.
- For MiniCPM-v2.6 and Qwen2-VL, the ASR and ASRG increase with the number of multimodal in-context samples. When the number of in-context samples is 5, the growth trend slows down. In contrast, the adversarial robustness of LLaVA-NeXT is less effected by the number of multimodal in-context samples.
- Ours@image: A variant of our method with the adversarial image is removed in the optimization process.
- Ours@suffix t: A variant of our method with the transferbased strategy for the adversarial suffix is removed in the optimization process.
- Ours@image t: A variant of our method with the transfer-based strategy for the adversarial image is removed in the optimization process.

<!-- image -->

The ablation study results are shown in Table VI. We can have the following observations:

- Eliminating the optimization for either the adversarial suffix or image within our method results in a marked decrease in both ASR and ASR-G. This underscores the efficacy of interactive optimization between adversarial suffixes and images, which yields improved performance compared to single-modality adversarial optimization.
- Observations from the ASR-G of Ours@suffix and Ours@image experiments reveal that the removal of optimization for either the adversarial suffix or image differentially impacts various MLLMs. Specifically, LLaVA7B exhibits heightened sensitivity to the removal of adversarial image optimization, whereas MiniGPT-v2 and MiniGPT4 demonstrate greater robustness to the absence of adversarial suffix optimization in the ASR-G metric. This distinction underscores the enhanced adaptability of multimodal jailbreak attacks to exploit specific weaknesses across different MLLM architectures.
- Both the transfer-based strategy for the adversarial image and the corresponding strategy for the adversarial suffix contribute to enhancing the success rate of universal jailbreak attacks in a black-box scenario. Notably, the strategy applied to the adversarial image proves to be more effective than its suffix counterpart in improving attack outcomes.
- In conclusion, our approach integrates textual and visual jailbreak attacks into a unified framework, leveraging a transfer-based strategy for classification tasks to enhance the transferability of multimodal universal jailbreak attack samples. The efficiency of each component of the proposed method is evidenced by the data presented in Table VI.

## GLYPH&lt;0&gt;YGLYPH&lt;0&gt;LGLYPH&lt;0&gt;FGLYPH&lt;0&gt;WGLYPH&lt;0&gt;LGLYPH&lt;0&gt;PGLYPH&lt;0&gt;¶GLYPH&lt;0&gt;VGLYPH&lt;0&gt;GLYPH&lt;3&gt;GLYPH&lt;0&gt;QGLYPH&lt;0&gt;DGLYPH&lt;0&gt;PGLYPH&lt;0&gt;HGLYPH&lt;0&gt;«GLYPH&lt;0&gt;« D. In-depth analyses.

Fig. 6: Illustration of multimodal in-context jailbreak attacks.

## C. Ablation Study

we compare variants of our method from the following perspectives: (1) the impact of different components in our method. (2) the effect of the transfer-based strategy in our method. The following variants of our method are designed for comparison.

To further elucidate the proposed method, we compared its performance with the Text&amp;Image method 1 . As shown in Figure 9, our method consistently outperforms Text&amp;Image in both ASR and ASR-G metrics. This result highlights the risks associated with image-text modality interactions in undesirable MLLM outputs. Overall, the proposed method demonstrates stable superiority over the simple combination of adversarial suffixes and adversarial images.

- Ours@suffix: A variant of our method with the adversarial suffix is removed in the optimization process.
- 1 Text&amp;Image: This approach combines the adversarial suffix generated by GCG with the adversarial image from Visual-Jailbreak, without utilizing image-text interaction.

TABLE V: We use Minigpt-v2-7b as the surrogate model and evaluate the effect of jailbreak attacks in a multimodal in-context learning setting.

| Number of in-context samples   | Jailbreak Attacks          | LLaVA-NeXT -7B   | LLaVA-NeXT -7B   | MiniCPM-V2.6 -8B   | MiniCPM-V2.6 -8B   | Qwen2-VL -8B   | Qwen2-VL -8B   | GPT-4O -1023   | GPT-4O -1023   |
|--------------------------------|----------------------------|------------------|------------------|--------------------|--------------------|----------------|----------------|----------------|----------------|
| Number of in-context samples   | Jailbreak Attacks          | ASR ↑            | ASR-G ↑          | ASR ↑              | ASR-G ↑            | ASR ↑          | ASR-G ↑        | ASR ↑          | ASR-G ↑        |
| 1                              | GCG Visual- jailbreak Ours | 52.0 28.0 61.0   | 32.0 22.0 38.0   | 21.0 28.0 48.0     | 21.0 28.0 40.0     | 17.0 15.0 25.0 | 17.0 14.0 23.0 | 4.0 1.0 3.0    | 3.0 0.0        |
| 2                              | GCG Visual- jailbreak Ours | 52.0 36.0 62.0   | 46.0 31.0        | 36.0 30.0 54.0     | 36.0 29.0 41.0     | 27.0 17.0 45.0 | 26.0 16.0 42.0 | 4.0 0.0        | 2.0 2.0 0.0    |
| 3                              | GCG Visual- jailbreak Ours | 50.0 36.0        | 40.0 44.0 33.0   | 70.0 45.0          | 69.0 41.0          | 40.0 32.0      | 38.0 27.0      | 3.0 6.0        | 2.0 3.0 0.0    |
| 4                              | GCG Visual- jailbreak      | 62.0 51.0 36.0   | 42.0 44.0 28.0   | 90.0 68.0 66.0     | 88.0 68.0 63.0     | 53.0 48.0      | 51.0 47.0      | 2.0 7.0 1.0    | 4.0 0.0        |
|                                | Ours                       | 62.0             | 42.0             | 89.0               | 90.0               | 38.0 58.0      | 30.0 55.0      | 2.0 4.0        | 0.0 2.0        |

<!-- image -->

Fig. 7: Examples of multimodal universal jailbreak attack on LLaVA-7B and LLaVA-13B

<!-- image -->

TABLE VI: Ablation study. Evaluation of the proposed method on different MLLMs where the surrogate model is LLaVA-7B.

|               | Victim Models   | Victim Models   | Victim Models    | Victim Models    | Victim Models   | Victim Models   |
|---------------|-----------------|-----------------|------------------|------------------|-----------------|-----------------|
| Variants      | LLaVA 7B(%)     | LLaVA 7B(%)     | MiniGPT-v2 7B(%) | MiniGPT-v2 7B(%) | MiniGPT4 7B(%)  | MiniGPT4 7B(%)  |
|               | ASR             | ASR-G           | ASR              | ASR-G            | ASR             | ASR-G           |
| Ours@image    | 15.0            | 10.0            | 66.0             | 25.0             | 39.0            | 32.0            |
| Ours@suffix   | 80.0            | 70.0            | 90.0             | 15.0             | 71.0            | 27.0            |
| Ours@suffix t | 88.0            | 80.0            | 99.0             | 52.0             | 92.0            | 60.0            |
| ours@image t  | 86.0            | 79.0            | 99.0             | 50.0             | 90.0            | 58.0            |
| Ours          | 88.0            | 80.0            | 100.0            | 55.0             | 95.0            | 64.0            |

by malicious actors, exploit different stages of the LLM lifecycle. Jailbreak attacks often exploit robustness gaps through input perturbations or transformation of expression. For instance, Zou et al. [8] demonstrated the efficacy of token-level optimization for creating adversarial suffixes that prompt negative behavior in models. Yuan et al. [9] uncovered that non-natural language prompts could bypass safety mechanisms primarily designed for natural language processing.

## E. Discussion

Here, we provide a discussion on several issues related to this work.

## •

- The vulnerabilities in LLMs and MLLMs.
- 1). The vulnerabilities in LLMs arise from two main sources: inherent issues and targeted attacks. Inherent issues, such as performance weaknesses and sustainability challenges, stem from the limitations of LLMs themselves, which can be mitigated over time with more data and improved training methods. Targeted attacks, initiated

2). Building on the advancements of LLMs, researchers have extended their capabilities to handle multiple modalities through various multimodal fusion approaches. However, while MLLMs demonstrate significant multimodal potential, they are likely to inherit the vulnerabilities of LLMs [37]. Additionally, the unique risks posed by images present further challenges [22], [40], [41]. In this work, the proposed method explores the vulnerability of MLLMs that utilize image-text interaction to distribute harmful information across adversarial images and suffixes, which provides a new insight for the safety risks of MLLMs.

Fig. 8: Examples illustrating that ASR and ASR-G evaluate the same output differently.

<!-- image -->

- Security risks in the interaction of image and text modalities. While many studies concentrate on jailbreak attacks through language spaces and image content, our analysis highlights significant security risks stemming from multimodal interactions in MLLMs. The primary objective of MLLMs-to accurately interpret and respond to multimodal contexts-enables attackers to exploit these systems by distributing jailbreak information across both image and text inputs, thereby effectively bypassing MLLM defense mechanisms. Building on this understanding, our method specifically targets MLLMs that integrate information across visual and textual inputs. By simultaneously manipulating both modalities, our multimodal adversarial examples leverage the intricate dependencies and interactions between them. For instance, manipulating images and texts together through imagetext interactions can more effectively induce MLLMs to respond and bypass safety checks than altering either modality independently. This exploitation of complex interdependencies, absent in single-modal scenarios, makes our multimodal jailbreak attacks particularly not easy to detect and defend.
- Defending Against Image-Text Interaction-Based Jailbreak Attacks. Since the discovery of jailbreak attacks, defense mechanisms have evolved, encompassing systemlevel and model-level approaches. System-level defenses add external safety layers to filter harmful prompts. For example, smoothLLM [42] generates multiple outputs from modified prompts, selecting the safest response through majority voting. Model-level defenses focus on modifying the LLM itself, using strategies such as safety training [43], refusal mechanisms [44], and adversarial training [45]. To counteract jailbreak attacks exploiting image-text interactions in MLLMs, we propose three potential defenses:
- 1). Cross-Modal Adversarial Fine-Tuning: Unlike traditional fine-tuning against adversarial images or text, this approach targets attacks that exploit both modalities

together. By fine-tuning the model with adversarial examples specifically crafted for image-text interactions, we enhance robustness in the image-text alignment space, making the model more resistant to these multimodal adversarial attacks.

## 2). Multimodal Input Sanitization:

Preprocessing and Filtering : Implement preprocessing layers that filter adversarial noise from both image and text inputs. Techniques such as noise detection, input sanitization, and adversarial detection algorithms help identify manipulated inputs before they reach the model. Universal Adversarial Sample Detection: Train a detector model to identify adversarial patterns across modalities, including pixel-level manipulations in images and token-level alterations in text, which are commonly used to bypass safety mechanisms.

- 3). Dynamic Contextual Analysis: Continuously monitor the semantic and logical coherence of image-text interactions. If inputs appear adversarial or nonsensical when processed together, the model can reject or flag these interactions as potentially harmful.
- Limitations of this work. Although our method demonstrates enhanced effectiveness compared to baseline approaches, the attack success rate diminishes as the size of MLLMs increases. This decline is attributable to the simpler multimodal alignment space in smaller models like the LLaVA-7B, which does not generalize well to larger MLLMs such as the 34B or GPT-4. Resource constraints preclude the use of the larger models as a surrogate in our experiments.

## F. Visualization Results

To show the efficacy of multimodal universal jailbreak attacks, we present two illustrative examples employing both adversarial suffix and image in Figure 7. The outcomes from these MLLMs demonstrate that our approach not only successfully compels the LLaVA models to attempt to execute the specified behaviors but also enables models with varying

Fig. 9: Comparison between the proposed method and image&amp;text method. We utilize the multimodal adversarial image and suffix from MiniGPT-v2-7B to evaluate LLaVa-7B, MiniGPT4-7B, instructBLIP-7B, mPLUIG-Owl2-7B and MiniCPM-v2.5-8B. Text&amp;Image means that we simply combine the adversarial suffix from GCG and the adversarial image from Visual-jailbreak.

<!-- image -->

parameter sizes to generate responses that precisely align with the malicious instructions. Such results underscore the effectiveness and versatility of our proposed method. Furthermore, to illustrate that ASR-G is stealthier and more robust than ASR, we present examples in Fig 8(a) showing that even when models do not explicitly reject toxic instructions, their responses may not align with the attacker's objectives. Additionally, we illustrate in Fig 8(b) how overly long suffixes, such as those generated by GCG with a length of 20, can obscure the original instruction or result in responses in other languages. This evidence highlights ASR-G's capability to utilize GPT-4 in determining whether a response accurately fulfills a malicious instruction, rather than simply detecting the absence of a rejection phrase. More examples can be found in Appendix III

## VI. CONCLUSION

In this study, we introduce a multimodal universal jailbreak attack method that integrates image-based and suffix-based jailbreak attacks into a unified framework. Through iterative image-text interactions, this framework optimizes both the universal adversarial suffix and image, while a transfer-based strategy is employed to enhance their transferability across models. Experimental results demonstrate the superior performance of our approach over existing baselines, highlighting how the interplay between new and traditional modalities poses significant security challenges for Multimodal Large Language Models.

## REFERENCES

- [1] R. OpenAI, 'Gpt-4 technical report. arxiv 2303.08774,' View in Article , vol. 2, no. 5, 2023.
- [2] G. Team, R. Anil, S. Borgeaud, Y. Wu, J.-B. Alayrac, J. Yu, R. Soricut, J. Schalkwyk, A. M. Dai, A. Hauth et al. , 'Gemini: a family of highly capable multimodal models,' arXiv preprint arXiv:2312.11805 , 2023.
- [3] S. Yin, C. Fu, S. Zhao, K. Li, X. Sun, T. Xu, and E. Chen, 'A survey on multimodal large language models,' arXiv preprint arXiv:2306.13549 , 2023.
- [4] H. Liu, C. Li, Q. Wu, and Y. J. Lee, 'Visual instruction tuning,' Advances in neural information processing systems , vol. 36, 2024.
- [5] K. Li, Y. He, Y. Wang, Y. Li, W. Wang, P. Luo, Y. Wang, L. Wang, and Y. Qiao, 'Videochat: Chat-centric video understanding,' arXiv preprint arXiv:2305.06355 , 2023.
- [6] S. Deshmukh, B. Elizalde, R. Singh, and H. Wang, 'Pengi: An audio language model for audio tasks,' Advances in Neural Information Processing Systems , vol. 36, pp. 18 090-18 108, 2023.
- [7] C. Li, C. Wong, S. Zhang, N. Usuyama, H. Liu, J. Yang, T. Naumann, H. Poon, and J. Gao, 'Llava-med: Training a large language-and-vision assistant for biomedicine in one day,' Advances in Neural Information Processing Systems , vol. 36, 2024.
- [8] A. Zou, Z. Wang, J. Z. Kolter, and M. Fredrikson, 'Universal and transferable adversarial attacks on aligned language models,' arXiv preprint arXiv:2307.15043 , 2023.
- [9] Y. Yuan, W. Jiao, W. Wang, J.-t. Huang, P. He, S. Shi, and Z. Tu, 'Gpt4 is too smart to be safe: Stealthy chat with llms via cipher,' arXiv preprint arXiv:2308.06463 , 2023.
- [10] P. Chao, A. Robey, E. Dobriban, H. Hassani, G. J. Pappas, and E. Wong, 'Jailbreaking black box large language models in twenty queries,' arXiv preprint arXiv:2310.08419 , 2023.
- [11] X. Qi, K. Huang, A. Panda, M. Wang, and P. Mittal, 'Visual adversarial examples jailbreak aligned large language models,' in The Second Workshop on New Frontiers in Adversarial Machine Learning , 2023.
- [12] H. Liu, C. Li, Q. Wu, and Y. J. Lee, 'Visual instruction tuning,' 2023.
- [13] . AI, :, A. Young, B. Chen, C. Li, C. Huang, G. Zhang, G. Zhang, H. Li, J. Zhu, J. Chen, J. Chang, K. Yu, P. Liu, Q. Liu, S. Yue, S. Yang, S. Yang, T. Yu, W. Xie, W. Huang, X. Hu, X. Ren, X. Niu, P. Nie, Y. Xu, Y. Liu, Y. Wang, Y. Cai, Z. Gu, Z. Liu, and Z. Dai, 'Yi: Open foundation models by 01.ai,' 2024.
- [14] J. Chen, D. Zhu, X. Shen, X. Li, Z. Liu, P. Zhang, R. Krishnamoorthi, V. Chandra, Y. Xiong, and M. Elhoseiny, 'Minigpt-v2: large language model as a unified interface for vision-language multi-task learning,' arXiv preprint arXiv:2310.09478 , 2023.
- [15] D. Zhu, J. Chen, X. Shen, X. Li, and M. Elhoseiny, 'Minigpt-4: Enhancing vision-language understanding with advanced large language models,' arXiv preprint arXiv:2304.10592 , 2023.
- [16] W. Dai, J. Li, D. Li, A. M. H. Tiong, J. Zhao, W. Wang, B. Li, P. N. Fung, and S. Hoi, 'Instructblip: Towards general-purpose visionlanguage models with instruction tuning,' Advances in Neural Information Processing Systems , vol. 36, 2024.
- [17] P. Wang, S. Bai, S. Tan, S. Wang, Z. Fan, J. Bai, K. Chen, X. Liu, J. Wang, W. Ge et al. , 'Qwen2-vl: Enhancing vision-language model's perception of the world at any resolution,' arXiv preprint arXiv:2409.12191 , 2024.
- [18] Q. Ye, H. Xu, J. Ye, M. Yan, A. Hu, H. Liu, Q. Qian, J. Zhang, and F. Huang, 'mplug-owl2: Revolutionizing multi-modal large language model with modality collaboration,' in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition , 2024, pp. 13 040-13 051.
- [19] Y. Yao, T. Yu, A. Zhang, C. Wang, J. Cui, H. Zhu, T. Cai, H. Li, W. Zhao, Z. He et al. , 'Minicpm-v: A gpt-4v level mllm on your phone,' arXiv preprint arXiv:2408.01800 , 2024.
- [20] W. Wang, Q. Lv, W. Yu, W. Hong, J. Qi, Y. Wang, J. Ji, Z. Yang, L. Zhao, X. Song et al. , 'Cogvlm: Visual expert for pretrained language models,' arXiv preprint arXiv:2311.03079 , 2023.
- [21] X. Guo, F. Yu, H. Zhang, L. Qin, and B. Hu, 'Cold-attack: Jailbreaking llms with stealthiness and controllability,' arXiv preprint arXiv:2402.08679 , 2024.
- [22] Z. Niu, H. Ren, X. Gao, G. Hua, and R. Jin, 'Jailbreaking attack against multimodal large language model,' arXiv preprint arXiv:2402.02309 , 2024.
- [23] Y. Ran, W. Wang, M. Li, L.-C. Li, Y.-G. Wang, and J. Li, 'Cross-shaped adversarial patch attack,' IEEE Transactions on Circuits and Systems for Video Technology , vol. 34, no. 4, pp. 2289-2303, 2024.
- [24] T. Wang, L. Zhu, Z. Zhang, H. Zhang, and J. Han, 'Targeted adversarial attack against deep cross-modal hashing retrieval,' IEEE Transactions on Circuits and Systems for Video Technology , vol. 33, no. 10, pp. 61596172, 2023.

[25] A. Tao, Y. Duan, Y. Wang, J. Lu, and J. Zhou, 'Dynamics-aware adversarial attack of adaptive neural networks,' IEEE Transactions on Circuits and Systems for Video Technology , vol. 34, no. 7, pp. 55055518, 2024.

[26] Y. Wang, W. Hu, and R. Hong, 'Iterative adversarial attack on imageguided story ending generation,' IEEE Transactions on Multimedia , 2023.

[27] T. Chen and Z. Ma, 'Toward robust neural image compression: Adversarial attack and model finetuning,' IEEE Transactions on Circuits and Systems for Video Technology , vol. 33, no. 12, pp. 7842-7856, 2023.

[28] J. Zhang, Q. Yi, and J. Sang, 'Towards adversarial attack on visionlanguage pre-training models,' in Proceedings of the 30th ACM International Conference on Multimedia , 2022, pp. 5005-5013.

[29] Y. Wang, W. Hu, Y. Dong, and R. Hong, 'Exploring transferability of multimodal adversarial samples for vision-language pre-training models with contrastive learning,' arXiv preprint arXiv:2308.12636 , 2023.

[30] T. Qiao, B. Zhao, R. Shi, M. Han, M. Hassaballah, F. Retraint, and X. Luo, 'Scalable universal adversarial watermark defending against facial forgery,' IEEE Transactions on Information Forensics and Security , 2024.

[31] A. Liu, L. Pan, X. Hu, S. Li, L. Wen, I. King, and S. Y. Philip, 'An unforgeable publicly verifiable watermark for large language models,' in The Twelfth International Conference on Learning Representations , 2023.

[32] T. Qiao, Y. Ma, N. Zheng, H. Wu, Y. Chen, M. Xu, and X. Luo, 'A novel model watermarking for protecting generative adversarial network,' Computers &amp; Security , vol. 127, p. 103102, 2023.

[33] Y. Zhang, Y. Huang, Y. Sun, C. Liu, Z. Zhao, Z. Fang, Y. Wang, H. Chen, X. Yang, X. Wei et al. , 'Benchmarking trustworthiness of multimodal large language models: A comprehensive study,' arXiv preprint arXiv:2406.07057 , 2024.

[34] X. Wei, B. Pu, J. Lu, and B. Wu, 'Visually adversarial attacks and defenses in the physical world: A survey,' arXiv preprint arXiv:2211.01671 , 2022.

[35] S. Song, X. Li, and S. Li, 'How to bridge the gap between modalities: A comprehensive survey on multimodal large language model,' arXiv preprint arXiv:2311.07594 , 2023.

[36] A. Madry, A. Makelov, L. Schmidt, D. Tsipras, and A. Vladu, 'Towards deep learning models resistant to adversarial attacks,' arXiv preprint arXiv:1706.06083 , 2017.

[37] X. Qi, K. Huang, A. Panda, P. Henderson, M. Wang, and P. Mittal, 'Visual adversarial examples jailbreak aligned large language models,' in Proceedings of the AAAI Conference on Artificial Intelligence , vol. 38, no. 19, 2024, pp. 21 527-21 536.

[38] X. Wang and K. He, 'Enhancing the transferability of adversarial attacks through variance tuning,' in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition , 2021, pp. 1924-1933.

[39] A. Paszke, S. Gross, F. Massa, A. Lerer, J. Bradbury, G. Chanan, T. Killeen, Z. Lin, N. Gimelshein, L. Antiga et al. , 'Pytorch: An imperative style, high-performance deep learning library,' Advances in neural information processing systems , vol. 32, 2019.

- [40] E. Shayegani, Y. Dong, and N. Abu-Ghazaleh, 'Jailbreak in pieces: Compositional adversarial attacks on multi-modal language models,' in The Twelfth International Conference on Learning Representations , 2023.

[41] Z. Ying, A. Liu, T. Zhang, Z. Yu, S. Liang, X. Liu, and D. Tao, 'Jailbreak vision language models via bi-modal adversarial prompt,' arXiv preprint arXiv:2406.04031 , 2024.

[42] A. Robey, E. Wong, H. Hassani, and G. J. Pappas, 'Smoothllm: Defending large language models against jailbreaking attacks,' arXiv preprint arXiv:2310.03684 , 2023.

- [43] Z. Wang, F. Yang, L. Wang, P. Zhao, H. Wang, L. Chen, Q. Lin, and K.-F. Wong, 'Self-guard: Empower the llm to safeguard itself,' arXiv preprint arXiv:2310.15851 , 2023.
- [44] Y. Yuan, W. Jiao, W. Wang, J.-t. Huang, J. Xu, T. Liang, P. He, and Z. Tu, 'Refuse whenever you feel unsafe: Improving safety in llms via decoupled refusal training,' arXiv preprint arXiv:2407.09121 , 2024.
- [45] S. Xhonneux, A. Sordoni, S. G¨ unnemann, G. Gidel, and L. Schwinn, 'Efficient adversarial training in llms with continuous attacks,' arXiv preprint arXiv:2405.15589 , 2024.

Hanwang Zhang received the BEng.(Hons.) degree in computer science from Zhejiang University, Hangzhou, China, in 2009, and a Ph.D. degree in computer science from the National University of Singapore (NUS), Singapore, in 2014. He is currently an associate professor with Nanyang Technological University, Singapore. His research interests include developing multi-media and computer vision techniques for efficient search and recognition of visual content. He received the Best Demo RunnerUp Award in ACM MM 2012 and the Best Student

<!-- image -->

Paper Award in ACM MM 2013. He was the recipient of the Best Ph.D. Thesis Award of the School of Computing, NUS, 2014. ' 2025 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission.GLYPH&lt;13&gt;GLYPH&lt;10&gt;See https://www.ieee.org/publications/rights/index.html for more information. Authorized licensed use limited to: Concordia University Library. Downloaded on May 21,2025 at 23:57:46 UTC from IEEE Xplore.  Restrictions apply.

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

Youze Wang received a B.S. and master's degree from the School of Computer Science and Information Engineering at Hefei University of Technology, Hefei, China, where he is currently working toward his Ph.D. degree. His research interests include multimodal computing and multimodal adversarial robustness in machine learning.

Wenbo Hu is an associate professor in Hefei University of Technology. He received a Ph.D. degree from Tsinghua University in 2018. His research interests lie in machine learning, especially probabilistic machine learning and uncertainty, generative AI, and AI security. He has published more than 20 peer-reviewed papers in prestigious conferences and journals, including NeurIPS, KDD, IJCAI, etc.

Yinpeng Dong received the B.S. and Ph.D. degrees from the Department of Computer Science and Technology, Tsinghua University. He is currently a Post-Doctoral Researcher with the Department of Computer Science and Technology, Tsinghua University. His research interests include the adversarial robustness of machine learning and deep learning. He received the Microsoft Research Asia Fellowship and the Baidu Fellowship.

Jing Liu received the BE and ME degrees in 2001 and 2004, respectively, from Shandong University, and the PhD degree from Institute of Automation, Chinese Academy of Sciences in 2008. Currently, she is an associate professor at the National Laboratory of Pattern Recognition, Institute of Automation, Chinese Academy of Sciences. Her research interests include machine learning, image content analysis and classification, multimedia information indexing and retrieval, etc

This article has been accepted for publication in IEEE Transactions on Circuits and Systems for Video Technology. This is the author's version which has not been fully edited and content may change prior to final publication. Citation information: DOI 10.1109/TCSVT.2025.3526248

15

<!-- image -->

Richang Hong (Member, IEEE) received a Ph.D. degree from the University of Science and Technology of China, Hefei, China, in 2008. He was a Research Fellow of the School of Computing at the National University of Singapore, from 2008 to 2010. He is currently a Professor at the Hefei University of Technology, Hefei. He is also with the Key Laboratory of Knowledge Engineering with Big Data (Hefei University of Technology), Ministry of Education. He has coauthored over 100 publications in the areas of his research interests, which include multimedia content analysis and social media. He is a member of the ACM and the Executive Committee Member of the ACM SIGMM China Chapter. He was a recipient of the Best Paper Award from the ACM Multimedia 2010, the Best Paper Award from the ACM ICMR 2015, and the Honorable Mention of the IEEE Transactions on Multimedia Best Paper Award. He has served as the Technical Program Chair of the MMM 2016, ICIMCS 2017, and PCM 2018. Currently, he is an Associate Editor of IEEE Transactions on Big Data, IEEE Transactions on Computational Social Systems, ACM Transactions on Multimedia Computing Communications and Applications, Information Sciences (Elsevier), Neural Processing Letter (Springer), and Signal Processing (Elsevier).