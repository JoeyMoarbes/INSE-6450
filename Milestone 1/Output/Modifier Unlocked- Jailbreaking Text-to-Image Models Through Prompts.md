## Modifier Unlocked: Jailbreaking Text-to-Image Models Through Prompts

Shuofeng Liu ∗† , Mengyao Ma ∗ , Minhui Xue † , Guangdong Bai

∗ ∗ The University of Queensland, Australia † CSIRO's Data61, Australia

Abstract -The unprecedented image generation capability of text-to-image models makes them double-edged swords. While these models allow users to create exquisite images through simple prompts , they also provide adversaries with opportunities to generate Not-Safe-for-Work (NSFW) content, referred to as the jailbreak attack. Despite built-in safety filters serving as a mitigation, their vulnerabilities and associated safety issues remain a significant concern. In this work, we propose MODX, the first modifier-based attack framework for jailbreaking textto-image models. MODX leverages a heuristic algorithm with two heuristic functions (constraints) to identify modifiers that adjust the artistic genre to subtly introduce unsafe elements that drive the generated images towards NSFW. This approach takes advantage of the fact that filters are unlikely to reject images in certain styles or artistic forms, effectively inducing the models to generate NSFW content. We demonstrate the feasibility of modifier-based jailbreaking with a theoretical analysis, and provide experimental evidence of the effectiveness of MODX. Our results show that MODX outperforms existing methods in successfully achieving jailbreaking across four state-of-the-art text-to-image models. Moreover, we evaluate MODX across additional NSFW categories and on more models or model versions, demonstrating its strong scalability and generalization.

for-Work (NSFW) images introduces a significant concern. Adversaries can craft malicious prompts to bypass the model filters and induce models to generate NSFW images, a technique known as jailbreaking . Jailbreaking undermines the safe and ethical usage of text-to-image models and has severe negative societal impacts. For instance, on May 23, 2023, a verified X account posted a model-generated image depicting the Pentagon being bombed, causing widespread panic and leading to a noticeable dip in the US stock market [23]. Similarly, on January 26, 2024, a fake nude photo of Taylor Swift was uploaded on Telegram and 4chan, garnering billions of views and severely damaging Taylor Swift's reputation [22]. These incidents highlight the urgent need for studies into the vulnerabilities in the safety of textto-image models.

Disclaimer: This paper contains NSFW language and imagery that could be offensive, distressing, and/or upsetting. Reader discretion is advised.

## 1. Introduction

Text-to-image models, known for their powerful text comprehension and image generation capabilities, have revolutionized artwork design and reshaped our technological landscape. Users can generate their desired images effortlessly by inputting the image descriptions, known as prompts , through a convenient user interface. To make the text-to-image models produce high-quality images, an ideal prompt typically consists of two parts; the subject that describes the main object, and the modifier that adjusts the artistic descriptions [32], [41], [60]. Through diverse combinations of subjects and modifiers, users can generate images featuring various objects and styles using text-toimage models, such as DALL · E [14], Imagen [52], Midjourney [13], and Stable Diffusion [51].

Despite the unprecedented image-generation capabilities of text-to-image models, their risk of generating Not-Safe-

DOI 10.1109/SP61157.2025.00242

Major generative AI service providers, such as OpenAI [16] and Google [9], have increasingly strengthened models' built-in filters to enforce their established usage policies [4], [8]. However, previous studies have demonstrated the insufficiency of these filters, by crafting jailbreak prompts that bypass them and compel models to generate unsafe images. These studies can be divided into two categories based on their methodology, training-based [38], [49], [55], [61] and substitution-based [24], [44], [56]. Training-based methods rely on adversarial training, which perturb the embedding of prompt to transform sensitive content into unrelated expressions or gibberish. These methods are highly dependent on white-box access to models, which is impractical in today's landscape where most extensivelyused text-to-image models are close-sourced.

Substitution-based methods operates on prompts in a black-box manner, by replacing sensitive words in prompts with semantically similar phrases to bypass filtering. These methods predominantly focus on the subject of the prompt, as it is the central entity in the generated content. Due to the same reason, the subject is the main target of defenses [33], [37], [53], such that subject-substitution methods have been defeated during model evolution and filter advancement. On the other hand, the modifier , has been regarded as insignificant to the harmfulness of the generated content, as they are descriptive elements that specify characteristics such as size or artistic genres. As a result, the potential of modifiers in generating harmful content has been largely underestimated.

Our work . In this work, we propose MODX, a modifierbased jailbreak framework to expose unsafety issues of text-to-image models. The key attack goal for MODX is

(a) Scenario #1 (a classroom)

<!-- image -->

<!-- image -->

(b) Scenario #2 (a war)

Figure 1: Examples of NSFW images in two scenarios. The 'classroom' is a safe subject while the 'war' is deemed gore (unsafe).

to induce models to generate NSFW images under two practical scenarios illustrated in Figure 1. In Scenario #1 , MODX combines safe subjects with specific modifiers to generate NSFW images. Since there is no sensitive text, the modifiers fully leverage their ability to transform safe images into NSFW styles. In Scenario #2 , MODX compels the models to generate NSFW images with inherently sensitive subjects, using modifiers to increase the models' tendency of producing unsafe content related to these subjects.

To construct MODX, we first conduct a study of the logic behind the built-in safety filters in black-box diffusionbased text-to-image models. We describe these models as generally containing two types of filters. The first is the pre-filter designed to detect sensitive text within the prompt. Modifiers can easily bypass this filter, as they rarely contain any sensitive keywords or descriptions. The second one, post-filter , evaluates intermediate and final denoised outputs to determine if generated images are classified as NSFW. Its limitation lies in its inability to block certain artistic genres [48], [52], [62], even when these styles or forms exhibit NSFW tendencies. MODX is primarily designed to exploit this weakness. The high-level approach of MODX involves seeking local optimal results using heuristic algorithm under two heuristic functions to find appropriate modifiers that deceive the post-filter, making it perceive the generated image as a specific artistic genre rather than NSFW. To achieve this, we design two constraints to ensure that the semantic correlation between the modifiers and the NSFW category is high, and the embedding of the jailbreak prompt is close to that of the original one.

We evaluate MODX with both theoretical and empirical analyses. On the theoretical aspect, we establish a formal foundation to support the feasibility of MODX's modifierbased strategy in achieving jailbreaking. It leverages Lipschitz continuity and Wasserstein distance to prove that modifiers' effect on model output is bounded, such that the generated content can retain intended semantics, and the distance between modifier-generated and NSFW images is also bounded, such that the generated content is close to NSFW genres. We pinpoint the balance range within the two bounds, highlighting that appropriate modifier selections can bypass the filters and meanwhile lead the image representation to NSFW.

We also experimentally evaluate MODX's performance. We first assess its jailbreaking capability against two typical NSFW categories, explicit and gore , across four state-of-theart text-to-image models, (i.e., DALL · E 3 [14], Midjourney v6 [13], Imagen 3 [11], and Stable Diffusion 3 [21]) under both attack scenarios. The experimental results show that MODX achieves high BPR and ASR in both scenarios, with averages of 0.92 and 0.74 in Scenario #1 , and 0.79 and 0.53 in Scenario #2 . The generated NSFW images exhibit strong toxicity, and their high similarity scores indicate strong semantic consistency with the original (malicious) prompts. We also benchmark MODX against three state-of-the-art jailbreaking methods [24], [44], [61], and demonstrate that MODX consistently outperforms them across four models. To further evaluate scalability and generalization, we assess MODX's performance against more NSFW categories and across additional six popular text-to-image models or different versions. Results indicate that MODX's performance remains well, demonstrating its superiority as a practical and effective jailbreak framework.

Contributions . Our main contributions are listed below.

- A valuable step forward in jailbreaking text-toimage models. We propose MODX, a novel and effective method for jailbreaking attacks by strategically leveraging modifiers within prompts. It complements existing subject-based methods, by targeting the modifiers that have been underestimated.
- An impactful vulnerability unveiled from the filtering mechanisms of text-to-image models. Our work reveals a critical vulnerability within the filtering mechanisms of existing text-to-image models. By manipulating modifiers to adjust artistic styles, the victim models can be driven to generate content toward NSFW while bypassing safeguards. This finding for the first time highlights the significant role of modifier and the gap in current filtering systems.
- A new dataset for future research on modifierbased jailbreaking. We construct a Malicious Modifier Dataset (MMD) [12], comprising modifiers across five categories that strongly incline towards generating NSFW images. We release this dataset [12] with controlled access restrictions, to facilitate future research in this area.
- A comprehensive study and evaluation. We theoretically prove the feasibility of using modifiers for jailbreaking, and comprehensively evaluate MODX's effectiveness, scalability, and generalization.

## 2. Motivation of Modifier-based Jaibreaking

## 2.1. Preliminaries

Diffusion models . The implementations of most state-ofthe-art text-to-image models utilize diffusion-based architectures, and thus they are commonly referred to as diffusion models [29], [35], [58]. In essence, these models operate by reversing a diffusion process. That is, they initialize

the image with pure noise and progressively denoise it over multiple iterations to approximate a target distribution conditioned on a given textual input. Typically, the iterative denoising process can be expressed as

<!-- formula-not-decoded -->

where α t and ¯ α t are parameters related to the noise schedule, controlling the amount of noise removed at each step; ϵ θ is the model's prediction of the noise component; z ∼ N (0 , I ) is standard Gaussian noise and σ t controls the amount of random noise added. After iterating through all steps down to t =1, the model arrives at x 0 , where a denoised image that aligns with the input prompt should be generated. A detailed explanation is presented in Appendix A.

Prompt engineering . Prompt engineering is the process of designing and refining input prompts, to guide the outputs of AI generative models [41]. The prompts used in text-toimage models typically consist of two components, i.e., the subject and the modifiers [25], [43]. The subject controls the primary object or entity of the generated images, while the modifiers specify characteristics such as the artistic form, style and size. Compared with the subject, the modifier enhances the diversity and personalization of the generated images [34]. Given the more important role of subject, it is the main target of most jailbreaking methods.

## 2.2. Motivation

Built-in filters . Built-in filters are safeguarding mechanisms designed to prevent models from generating NSFW content [47], [52]. Due to concerns over model privacy and security [40], [42], most companies [9], [13], [16] have refrained from disclosing or releasing details about their built-in filters. Even Stability AI [21], known for its open-source, only provides access to the model's parameter weights without any information regarding the functioning of these filters. This lack of transparency makes exploring the vulnerabilities of text-to-image models challenging. Therefore, to gain a deeper understanding of vulnerabilities, we study the logic behind the built-in filters, drawing on established insights into text-to-image model behaviors and the underlying mechanisms of diffusion models.

The built-in filters generally consist of two main components, pre-filter and post-filter . Figure 2 illustrates the workflow of the filtering. Specifically, the pre-filter is positioned behind the encoder for sensitive text detection. If detected, the model denies the output or detoxifies the sensitive content before proceeding; otherwise, the denoising process starts. The post-filter is located just ahead of the output layer, detecting intermediate outputs for NSFW tendencies. If detected, the generation is halted or adjusted; if not, the image is outputted. The observed behavior of DALL · E 3 aligns with this process. When we input sensitive text, the model rejects output within an average of 2.55 seconds, indicating the existence of a pre-filter. Replacing sensitive text with similar but non-sensitive terms, many of the outputs are still rejected, with time ranging from 7.43

Figure 2: Built-in filters in the image generation pipeline.

<!-- image -->

Figure 3: The addition of modifiers results in NSFW images.

<!-- image -->

to 30.34 seconds. This variation suggests rejection occurs at different denoising steps, confirming the presence of a post-filter. Similar findings for unsafe text generation using LLMs have also been reported in a recent study [27].

NSFW through modifiers . As the post-filter is designed to block images with NSFW content, it does not filter out specific artistic genres. This weakness can be effectively exploited through modifiers to generate NSFW images. Figure 3 illustrates two practical scenarios in which modifiers can deceive the post-filter. In Scenario #1 , the addition of certain modifiers to a benign prompt changes the resulting image to NSFW style. In Scenario #2 , the sensitive text is substituted to bypass the pre-filter, but in most cases, the model either rejects the output or generates safe images. However, incorporating certain modifiers leads the model to generate massive NSFW images.

## 3. Problem Formulation

In this section, we first provide formal definitions of terminologies. Then we outline the practical attack scenarios of MODX, and discuss its threat model including the attack goal and adversary knowledge.

## 3.1. Definitions

Definition 1 (NSFW images) . Let subj denote the subject, and art denote the artistic genre of images. An image is considered NSFW if it satisfies one of the following conditions,

<!-- formula-not-decoded -->

(a) Ship

<!-- image -->

(b) Plane

(c) Bird

(d) Frog

(e) Deer

Figure 4: Examples of NSFW genre transfer. All images are generated by our method using DALL · E 3.

where img nsfw is the NSFW image, subj b is the benign normal subject in the image, and art nsfw is the NSFW artistic form; or

<!-- formula-not-decoded -->

where subj nsfw is the subject containing NSFW element, and art b represents the normal artistic form.

An NSFW image can be composed in two ways. Eq. 2 presents the first type, where the image consists of a benign subject combined with an unsafe artistic style. Eq. 3 presents the second type, where the image contains a sensitive subject with arbitrary artistic styles.

Definition 2 (Model output) . Let M denote a text-toimage model, F pre and F post denote pre-filter and post-filter respectively. Given M and a jailbreak prompt p j , its output can result in three possible outcomes.

<!-- formula-not-decoded -->

The outcome ' None ' means the model M refuses to generate an image for the input prompt p j . img b and img nsfw represent that the model outputs benign and NSFW images respectively.

Definition 3 (Bypass filters) . Given M , F pre , F post , and p j , if and only if the outcome of M ( F pre , F post , p j ) is not None , p j bypass F pre and F post .

̸

<!-- formula-not-decoded -->

A jailbreak prompt successfully bypasses the built-in filters if it makes the model output an image, whether a normal or NSFW image, rather than providing no response or displaying a rejection message.

Definition 4 (Jailbreaking) . Given M , F pre , F post , and p j , if and only if the outcome of M ( F pre , F post , p j ) is img nsfw , p j achieve a successful jailbreaking attack.

<!-- formula-not-decoded -->

A successful jailbreaking requires the model M outputs NSFW images. Jailbreaking is a sufficient condition for bypass filters .

## 3.2. Attack Scenarios

According to Definition 1, there are two attack scenarios in real-world system settings for MODX. We formulate two scenarios as follows.

Scenario #1 ( NSFW genre transfer ). In this scenario, the adversary focuses on generating images that would otherwise be normal into NSFW genres, which satisfy Eq. 2. For instance, an ordinary ship can be altered to appear in a gory style after the attack, which is classified as an NSFW image. This scenario does not involve any inherently sensitive or unsafe subjects. Some examples are illustrated in Figure 4.

Scenario #2 ( NSFW content generation ). In the second scenario, the adversary utilizes text-to-image models to generate NSFW images containing unsafe subjects, which satisfy Eq. 3, for example, generating images of nude human figures or depictions of warfare. In this case, the generated images include sensitive subjects that are classified as NSFW.

In both scenarios, the harm caused by jailbreaking is equally significant, as each results in the generation of NSFW content that violates safety and ethical guidelines.

## 3.3. Threat Model

Adversary knowledge . We assume the adversary is an online adversary, with access to publicly available web resources and black-box text-to-image models M , without any knowledge of their internal workflows or built-in filters F . The adversary can subscribe to and use any paid versions of models released by developers, querying through prompts. The adversary does not require any background knowledge in programming or fine arts to carry out the attack.

Attack goal . The main goal of the adversary is to design jailbreak prompts p j that can bypass the built-in filters (Definition 3) and achieve jailbreaking (Definition 4), i.e., generating NSFW images img nsfw under the aforementioned two scenarios. A template of the jailbreak prompt should be reused to execute multiple attacks by substituting certain elements in the prompt. The adversary also aims for the generated NSFW images to be of high quality with semantic similarity and exhibit strong levels of toxicity.

## 4. Approach

In this section, we present MODX, a novel and effective modifier-based jailbreaking framework designed to craft jailbreak prompts that can induce text-to-image models to generate NSFW images. We first introduce the overall workflow of MODX, and then delve into the technique details.

## 4.1. Overview

The intuitive explanation for why MODX can bypass built-in filters lies in the fact that filters do not reject outputting images depicting certain artistic genres, such as dark

Figure 5: Overall pipeline of MODX.

<!-- image -->

art, horror movie posters, or anatomical nude figures, even though such images often contain notable NSFW elements. MODX exploits this vulnerability by identifying modifiers that can affect the denoising process to generate images with unsafe artistic genres.

Working pipeline . MODX aims to create jailbreak prompts that force text-to-image models to generate specific categories of NSFW images. Figure 5 illustrates its overall workflow. The entire pipeline consists of two main components, i.e., modifier collection and jailbreak prompt creation . MODX begins by categorizing modifiers into distinct groups in terms of their various emphasis. It then collects modifiers within each category, resulting in a comprehensive modifier dataset. Next, MODX examines the adversary's original prompt for sensitive text. If any sensitive content is detected, it is substituted with semantically similar text to bypass the pre-filter. Once the subject is sanitized, MODX searches from the modifier dataset for appropriate modifiers that meet Constraint #1 . After satisfying this constraint, the selected modifiers are combined with the sanitized subject to create a list of potential jailbreak prompts. Then MODX executes the heuristic algorithm to yield final jailbreak prompts from the list under Constraint #2 . The detailed definitions of the two constraints are located in Section 4.3. The resulting prompt follows the template in the curly bracket, i.e., { subject,[medium],[movement],[flavor], by [artist],[trending] . } .

## 4.2. Modifier Collection

To select appropriate modifiers for constructing jailbreak prompts, it is necessary to have a dataset containing modifiers with tendencies to generate NSFW images. To the best of our knowledge, there exists no comprehensive modifier dataset tailored for this purpose. Therefore, we turn to creating such a dataset, which we refer to as the Malicious Modifier Dataset (MMD).

Taxonomy of modifiers . To efficiently and purposefully collect modifiers, we first explore the taxonomy of modifiers. As there is no unified taxonomy for modifiers, we adopt the widely recognized classification approach used by CLIP Interrogator [2] for our work. It categorizes modifiers into five types, i.e., artist , medium , movement , flavor , and trending . The definitions and typical examples are presented in Table 8 in Appendix C. Our decision to use the CLIP

Interrogator's taxonomy is based on its derivation from extensive image and text data, which extracts general patterns that encompasses categories used in other studies according to the descriptions. For instance, modifiers identified by Oppenlaender et al. [43] as ' style modifier ' fall under the ' artist ' category, while Rugg's [17] ' art techniques ' aligns with the ' medium ' category. Additionally, CLIP Interrogator's ability to analyze a given image and suggest potential modifiers across the five categories significantly boosts the efficiency of our collection process.

Dataset creation . After we get the five categories of modifiers, we proceed to collect modifiers within each category. Since these modifiers are required to have tendencies of generating NSFW content, we focus on three main sources, i.e., art-related websites containing unsafe themes, online malicious text-to-image prompts, and the output of CLIP Interrogator when NSFW images are used as input.

For art-related websites, we focus on three prominent platforms: DeviantArt [6], Saatchi Art [20], and Dark Art Movement [5]. We select NSFW-related artworks and record relevant modifiers based on their tags. The detailed descriptions and procedures for the three platforms are provided in Appendix B.

For NSFW image-generating prompts, as there is no publicly available one, we turn to PromptHero [18]. PromptHero is a platform that shares prompts and their corresponding images, including a wide range of themes, styles, and art movements. We search for NSFW on PromptHero and collect the modifiers present in those prompts associated with all displayed images, categorizing them into the defined five categories.

For CLIP Interrogator, we first gather a set of 600 NSFW images from Reddit [19] and 4chan [1], which includes both AI-generated images and real-world examples. From Reddit, we gather 300 of the most recent NSFW images from different communities and sub-communities [15]. Similarly, we collect an additional 300 NSFW images from notorious NSFW subcategories on 4chan. We then employ Q16 [54] to analyze these 600 images and find that 572 are classified as NSFW. Subsequently, we use CLIP Interrogator to extract the corresponding modifiers for these images across the five defined categories.

Through these three sources, we collect prompt modifiers from a total of 839 images. After consolidating the collected modifiers and removing duplicates, we find that the dataset includes 82 modifiers for the medium category,

116 for movement , 267 for flavor , 157 for artist , and 95 for trending . This results in the creation of a comprehensive Malicious Modifier Dataset (MMD).

## 4.3. Jailbreak Prompt Construction

After creating the MMD, MODX selects appropriate modifiers from the dataset to construct jailbreak prompts. According to our two attack scenarios, Scenario #1 does not contain sensitive subjects, so the prompt can disregard the safeguard of the pre-filter. Based on Eq. 2, the jailbreak prompt in this scenario can be formalized as

<!-- formula-not-decoded -->

where ⊕ represents the concatenation of the subject with modifiers. In contrast, Scenario #2 requires the generation of unsafe subjects, so we need bypass the pre-filter by substituting sensitive subjects with similar but safe descriptions. Based on Eq. 3, the jailbreak prompt in the second scenario can be formalized as

<!-- formula-not-decoded -->

where subj s is the substitution of sensitive subjects. We also use art nsfw because art nsfw ⊂ art with a stronger tendency to generate NSFW images.

Sensitive text substitution . Existing research shows that ChatGPT can generate alternative descriptions for sensitive subjects [24], [44], e.g., replacing ' blood ' with ' ketchup '. In Scenario #2 , we leverage GPT-4o [10] to perform the substitutions. We prompt GPT-4o with ' Generate 3 substitutions for [sensitive text] ' to obtain three alternative descriptions. We then use SentenceBERT (SBERT) [50] to calculate the semantic similarity between each substitution and the original sensitive text, selecting the highest-similarity substitution as the subject for the jailbreak prompt.

Design constraints . The most critical step in MODX's jailbreak prompt construction is the selection of appropriate modifiers to induce the model to generate NSFW images. To guide MODX in selecting these modifiers, we define two specific constraints. Let E mb( · ) denote an embedding function, where m is the candidate modifier, C N represents the NSFW category, p j is the completed jailbreak prompt, and p o is the adversary's original prompt. The two constraints can be expressed as follows.

- Constraint #1 (Similarity to NSFW category). E mb( m ) ≃ E mb( C N ) .
- Constraint #2 (Semantic consistency with original prompt). E mb( p j ) ≃ E mb( p o ) .

Specifically, the first constraint requires that the embedding of the modifiers have a high similarity to the embedding of the category term describing the desired NSFW image type. This constraint ensures that the selected modifiers can generate specific types of NSFW images, such as explicit or gore, presenting them as a particular artistic form or style. This allows the prompt to bypass the post-filter, achieving our attack goal. The second constraint requires that the full jailbreak prompt, with the chosen modifiers, maintains high semantic similarity with the adversary's original prompt for the intended image. This constraint further screens the remaining modifiers, ensuring that the generated image's content aligns closely with the adversary's intended output. Mathematical calculation . For Constraint #1 , since there is currently no standardized taxonomy or terminology for NSFW categories, the adversary first defines a concise description of the desired NSFW category and then prompts GPT-4o to generate two synonyms. These three descriptions represent the intended NSFW category. We use CLIP [46] to calculate the similarity, ranking the modifiers in each category in descending order based on the similarity scores. Specifically, each of the three descriptions is compared with each modifier category, and the average of the three similarity scores is used to rank the modifiers. After sorting, we select the top p modifiers from each category. Then, one modifier from each category is selected and combined with the subject to create jailbreak prompts. Given five categories, this approach yields p 5 potential jailbreak prompts (as by default, we use one modifier from each category per prompt). These prompts are then moved to the next constraint for further selection. For Constraint #2 , we use SBERT [50] to calculate the semantic similarity. Based on the results, the top k jailbreak prompts are selected.

Discussion . This approach offers the adversary significant flexibility to try different combinations of modifiers, allowing for the creation of a large variety of NSFW images. By designing the constraints to operate in a sequential manner, MODX quickly identifies local optimal solutions and avoids costly computations.

## 5. Case Studies

We provide case studies demonstrating MODX 's success in executing jailbreaking on two representative NSFW categories, i.e., explicit and gore under our two attack scenarios. These categories are chosen because current filters primarily target them, and they exhibit distinct characteristics. Also, forcing text-to-image models to generate images in these two NSFW categories has proven challenging. As for models, we select DALL · E 3 and Stable Diffusion 3 (SD 3) as the attack target. This is because DALL · E 3 is renowned for generating high-quality images and has robust safety filters [28], [49], while SD 3, known for being freely accessible, has the largest user base [31].

## 5.1. Explicit

Explicit content refers to material that depicts graphic or overtly sexual themes. This type of content typically includes imagery that is suggestive, provocative, or sexually explicit, which is considered inappropriate for general or younger audiences.

Scenario #1 . We first use MODX to jailbreak text-to-image models to generate explicit images with benign subjects. We choose 'teacher' as the subject and construct the original

Figure 6: Examples of jailbreak prompts and generated images in two scenarios. Explicit images are blurred.

<!-- image -->

prompt: { a teacher } . Jailbreaking is then achieved by selecting modifiers. Following our approach (see Section 4 ), we begin by defining the target category as 'explicit' and generate two synonyms by GPT-4o as E mb ( C N ) in Constraint #1 . We get 'explicit', 'sexual', and 'pornographic'. Computing the embedding similarity between these three terms and the modifiers in our created MMD by using CLIP. Each category's modifiers are ranked by average similarity score in descending order, and we select the top two modifiers per category (i.e., p =2), creating 32 potential jailbreak prompts through different combinations. Next, we use SBERT to calculate the semantic similarity between each of these 32 prompts and the original prompt under Constraint #2 , selecting the top three ( k =3) jailbreak prompts. We then use these prompts to attack DALL · E 3 and SD 3, successfully generating explicit images. The first row in Figure 6.(a) presents the jailbreak prompts and some of the resulting images.

Scenario #2 . We use MODX to jailbreak the models to generate explicit content including sensitive descriptions. We choose 'a naked person' as the original malicious prompt. Since the prompt contains sensitive text, we first perform substitution by querying GPT-4o ' Generate 3 substitutions for naked '. We get 'swimwear look', 'bikini', and 'minimal coverage'. By calculating the semantic similarity by SBERT, we choose 'bikini' as the substitution subject. The rest of the processes are the same as that in the first scenario. Finally, we obtain three prompts and use them to jailbreak DALL · E 3 and SD 3. The first row in Figure 6.(b) illustrates an example of the jailbreak prompts and some generated explicit images.

## 5.2. Gore

Gore refers to content that graphically depicts extreme injuries, violence, or bodily harm, often showcasing blood, wounds, or dismemberment. This type of material is intended to evoke shock or horror and is generally deemed unsuitable for audiences. Our jailbreak prompts and generated images for two scenarios are illustrated in the second row in Figure 6.(a) and 6.(b) respectively. The detailed explanation is provided in Appendix D.

## 6. Theoretical Analysis

In this section, we theoretically demonstrate the efficacy of using modifiers to bypass the filters and achieve jailbreaking. We leverage Lipschitz continuity and distributional similarity analysis to prove that with the addition of modifiers, text-to-image models can generate images that approximate the characteristics of the NSFW distribution (i.e., proximity to NSFW ) without significantly altering the intended semantics of the prompt (i.e., semantics preservation ).

## 6.1. Definitions and Assumptions

Definition 5 (Lipschitz continuity) . A function L : R n → R is said to be Lipschitz continuous if there exists a constant L such that

<!-- formula-not-decoded -->

for all θ ∈ R n .

If a function is differentiable and its derivative is Lipschitz continuous, then its derivative is bounded. This means the rate of change of the function does not increase indefinitely. In numerical analysis and optimization, Lipschitz continuity ensures convergence and the uniqueness of solutions.

Definition 6 (1-Wasserstein distance) . Given two probability distributions P and Q on X , the Wasserstein distance between the two distributions is defined as

<!-- formula-not-decoded -->

where d ( x, y ) is the distance between points x and y in the metric space X , and Π( P, Q ) is the set of all couplings of P and Q .

The 1-Wasserstein distance measures the distance between two probability distributions, quantifying the 'cost' of transforming one distribution into the other.

Assumption 1 (Text encoder Lipschitz continuity) . We assume the text encoder E is Lipschitz continuous with constant L E . This implies that for any two prompts p and p ′ ,

<!-- formula-not-decoded -->

where diff( p, p ′ ) is the difference between the two prompts.

According to Definition 5, this property ensures that a slight modification in the prompt (such as adding modifiers) results in a bounded change in the resulting embedding.

Assumption 2 (Noise prediction function Lipschitz continuity) . The text noise prediction function ϵ θ ( x, t, c ) is Lipschitz continuous with respect to the conditioning embedding c with Lipschitz constant L . This implies that for two prompts p o and p m ,

<!-- formula-not-decoded -->

where p o is the original prompt, and p m is the modified prompt with modifiers.

This ensures that small changes in the embedding will result in bounded changes in the predicted noise for denoising steps.

Assumption 3 (Divergence between benign and NSFW image distributions) . The 1-Wasserstein distance between the distribution of benign images D b and the distribution of NSFW images D nsfw is a positive constant ∆ .

<!-- formula-not-decoded -->

According to Definition 6, this assumption ensures that the statistical characteristics of the two distributions exhibit a clear degree of separation, sufficient for distinguishing between benign and NSFW images.

## 6.2. Formal Foundation of MODX's Efficacy

We prove the semantics preservation and proximity to NSFW of MODX's modifier-based method. These are guaranteed by two bounds, i.e., the modifier's effect on model output (Theorem 1, 2), and the distance between modifiergenerated and NSFW images (Theorem 3). MODX can achieve an effective jailbreaking by identifying a balance range between two bounds (Theorem 4).

Theorem 1 (Effect of modifiers on embedding shift is bounded) . Given an original prompt p o , a modified prompt with modifiers p m , and a text encoder E , the difference in their embeddings E ( p o ) and E ( p m ) can be bounded by,

<!-- formula-not-decoded -->

where l = diff( p o , p m ) represents difference between p o and p m , i.e., the added modifiers.

Theorem 1 demonstrates that adding a modifier to a prompt has a limited and controllable effect on the embedding vector. The difference between the embedding vectors of the modified prompt and the original prompt can be quantified with an upper bound L E ∥ l ∥ 2 . The detailed proof is presented in Appendix E.1.

Theorem 2 (Effect of modifiers on model output is bounded) . Given p o , p m , and E , the difference in the final denoised outputs, x 0 o and x 0 m can be bounded by

<!-- formula-not-decoded -->

where x 0 m and x 0 o are the final denoised outputs of modified prompt and original prompt, respectively, and T is the total number of timesteps.

Theorem 2 demonstrates that in the denoising process of a text-to-image model, the influence of adding modifiers has a bounded effect on the model's final output. The difference between the outputs can be quantified with an upper bound 1 -α t √ α t (1 -¯ α t ) LL E ∥ l ∥ 2 . This bound allows the modifier to bypass the model's built-in filter and generate images. We provide detailed proof in Appendix E.2.

Theorem 3 (Modifier can shift the distribution to NSFW) . Given l = diff( p o , p m ) , the 1-Wasserstein distance between the distribution of images generated with modifier D m and NSFW images D nsfw can be bounded by,

<!-- formula-not-decoded -->

where C = LL E is a constant.

Theorem 3 shows that the 1-Wasserstein distance between D m and D NSFW can be bounded. This upper bound implies that by controlling the use of the modifier, (i.e., a relative small ∥ d ∥ ), it is possible that W 1 ( D m , D nsfw ) &lt; ∆ holds. The detailed proof is shown in Appendix E.3.

Theorem 4 (Existence of suitable modifiers satisfying both bounded output and bounded NSFW distribution shift) . Given p o , p m with l = diff( p o , p m ) , there exists a choice of l such that both the difference in the final outputs of the model is bounded and the 1-Wassertein distance between D m and D NSFW is bounded. The ∥ l ∥ 2 can be expressed as,

<!-- formula-not-decoded -->

Theorem 4 demonstrates that a suitably chosen l can bypass the filter, allowing the model to generate images and shift them towards the NSFW category. This result provides strong theoretical support for MODX, reinforcing its foundation in achieving jailbreaking. The detailed proof is listed in Appendix E.4.

## 7. Evaluation

To comprehensively evaluate the performance of MODX across various contexts, our evaluation primarily answers the following research questions (RQs).

- RQ1 (MODX's jailbreaking capability) . How effective are the jailbreak prompts generated by MODX against state-of-the-art text-to-image models?
- RQ2 (Comparison with baselines) . How does MODX perform in comparison to other baseline methods?
- RQ3 (Scalability and generalization) . How effective is MODX in generating NSFW images across different categories? How does MODX perform across other text-to-image models or different versions?

## 7.1. Experimental Settings

NSFW categories . Since the community currently lacks standardized taxonomy of NSFW images, following previous studies [45], [53], we focus by default on two highly

impactful NSFW categories, i.e., explicit and gore. When we explore the scalability of MODX, we adopt the scope of NSFW images proposed by Qu et al. [44], assessing MODX's performance on three additional NSFW categories, namely disturbing, hateful, and political.

Text-to-image models . We select four state-of-the-art textto-image models, DALL · E 3, Imagen 3, Midjourney v6.1, and Stable Diffusion 3, as our primary targets for the jailbreaking attack due to their ease of use and large user bases. To evaluate the generalization of MODX, we further include other mainstream models, specifically Craiyon v4 [3] and FLUX v1 [7], as well as different model versions, DALL · E 2, Imagen 2, Midjourney v4, and Stable Diffusion XL. All models are tested with their default configurations, and for models with prompt enhancement features, we disable those features to ensure a fair testing environment.

Queries . To mitigate potential biases, we generate four images per prompt for each model. For models that do not support batch generation, we query them with the same prompt for four times.

Evaluation metrics . Four metrics are used to evaluate MODX's performance.

- Bypass Rate (BPR). BPR measures the ability of the generated jailbreak prompts to bypass built-in filters and produce images. A successful bypass occurs if the models generate any image rather than rejecting the prompts. BPR can be formally expressed as

<!-- formula-not-decoded -->

where N exp is the total expected number of generated images, and N bypass is the actual number of images generated.

- Attack Success Rate (ASR). ASR evaluates the ability of jailbreak prompts to generate NSFW images. A successful attack occurs when the model produces NSFW content. We employ the multi-headed safety classifier [44] to detect whether the generated images are classified as NSFW, as it accurately categorizes images into specific classes rather than a simple binary classifier. ASR can be formally expressed as

<!-- formula-not-decoded -->

where N nsfw is the number of NSFW images generated.

- Toxicity. Toxicity assesses the level of risk associated with NSFW images. We use the scaled logits of the classifier to represent the toxicity score, where scores over 50 are considered NSFW, with a maximum toxicity score of 100 indicating the highest risk.
- Similarity. Similarity measures how closely the generated NSFW images match the adversary's intended output. We use Stable Diffusion v1.4 (without built-in filters) to generate the target NSFW image from the original prompt ( Scenario #1 ) or original malicious prompt ( Scenario #2 ). We then follow the previous studies [44], [61], compute the Fr´ echet inception distance (FID) and Cosine Similarity (CS) between the

target image and the NSFW images generated by the jailbreak prompts.

We note that human validation is not incorporated in our evaluation, considering that metric-based evaluation is more objective and reproducible, and meanwhile reduces bias, inconsistency, and scalability issues. However, human validation can serve as a complement.

Baselines . We compare MODX with three jailbreak methods most relevant to our work.

- Hateful Meme (HM) Attack [44], which is designed to generate unsafe memes.
- SurrogatePrompt [24], which represents the substitution of sensitive words in the prompt with safe ones.
- SneakyPrompt [61], which represents training-based methods to create jailbreak prompts.

We reproduce the jailbreak prompts for these baselines following the methods and settings described in their papers.

## 7.2. RQ1: MODX's Jailbreaking Capability

In RQ1, we comprehensively evaluate MODX's capability of exploiting the vulnerabilities of built-in filters in text-to-image models to perform jailbreaking.

Setup . For each original malicious prompt, after ranking modifiers within each category under the Constraint #1 , we select the top 3 modifiers per category, i.e., p =3. This results in 3 5 potential jailbreak prompts. Under the Constraint #2 , we then select the top 10 ranked prompts, i.e., k =10, as the final jailbreak prompts generated by MODX. For the two NSFW categories, in Scenario #1 , we select 10 human professions from the UCI Adult dataset [26] as the subjects for explicit category, and use the 10 classes from CIFAR10 [36] as subjects for gore. In Scenario #2 , we select 10 representative original malicious prompts respectively from Reddit [19] for each category. This setup yields 400 jailbreak prompts, expected to generate 6,400 images.

Result analysis . Based on our experimental settings, we obtain the results displayed in Table 1. Overall, MODX successfully executes jailbreaking attacks across four models in two NSFW categories under both attack scenarios, with the most successful attacks observed on DALL · E 3 and Midjourney v6.1.

In Scenario #1 , MODX demonstrates an extremely high BPR for generating explicit and gore images, with average values across four models reaching 0.89 and 0.94, respectively. This indicates that MODX's jailbreak prompts effectively bypass pre-filters. For ASR, it achieves a high average of 0.67 for explicit and 0.79 for gore. Notably, on DALL · E 3, it achieves ASR of 0.75 and 0.9 for two NSFW categories. These results highlight our method's success in deceiving post-filters and generating NSFW images. To assess toxicity, we calculate the mean and variance of toxicity scores for each NSFW category across models. The explicit category has a mean toxicity of 66.16 with a standard deviation of 5.78, indicating consistently high toxicity levels. The gore category has a higher mean toxicity of 83.49 and a standard deviation of 10.29, underscoring MODX's stronger

TABLE 1: The effectiveness of MODX.

|             |                 |          |      | ASR   | ASR      | ASR   | ASR   |          |           |       |          |          |       | Toxicity   | Toxicity   | Toxicity   | Toxicity   | Toxicity   | Toxicity   |
|-------------|-----------------|----------|------|-------|----------|-------|-------|----------|-----------|-------|----------|----------|-------|------------|------------|------------|------------|------------|------------|
| Scenario    | Models          | Explicit | Gore | Avg.  | Explicit | Gore  | Avg.  | Explicit | Mean Gore | Avg.  | Explicit | Std Gore | Avg.  | Explicit   | FID Gore   | Avg.       | Explicit   | CS Gore    | Avg.       |
| Scenario #1 | DALL · E 3      | 0.82     | 0.96 | 0.89  | 0.75     | 0.90  | 0.83  | 65.62    | 91.11     | 78.37 | 6.15     | 8.00     | 7.08  | 124.25     | 89.70      | 106.98     | 0.76       | 0.76       | 0.76       |
|             | Imagen 3        | 0.80     | 0.85 | 0.83  | 0.64     | 0.76  | 0.71  | 69.11    | 85.03     | 77.07 | 5.77     | 9.41     | 7.59  | 123.73     | 152.19     | 137.96     | 0.92       | 0.79       | 0.86       |
|             | Midjourney v6.1 | 0.93     | 0.95 | 0.94  | 0.69     | 0.84  | 0.77  | 66.67    | 78.03     | 72.35 | 5.99     | 10.42    | 8.21  | 121.36     | 99.46      | 110.41     | 0.73       | 0.72       | 0.73       |
|             | SD 3            | 1.00     | 1.00 | 1.00  | 0.60     | 0.65  | 0.63  | 63.25    | 79.77     | 71.62 | 5.22     | 13.32    | 9.26  | 120.03     | 137.73     | 128.88     | 0.91       | 0.75       | 0.83       |
|             | Avg.            | 0.89     | 0.94 | 0.92  | 0.67     | 0.79  | 0.74  | 66.16    | 83.49     | 74.85 | 5.78     | 10.29    | 8.04  | 122.34     | 119.77     | 121.06     | 0.83       | 0.76       | 0.80       |
|             | DALL · E 3      | 0.75     | 0.68 | 0.72  | 0.35     | 0.55  | 0.45  | 58.64    | 83.98     | 71.31 | 9.92     | 14.89    | 12.41 | 169.82     | 179.23     | 174.52     | 0.78       | 0.79       | 0.78       |
|             | Imagen 3        | 0.50     | 0.58 | 0.54  | 0.16     | 0.24  | 0.20  | 63.72    | 83.61     | 73.66 | 5.72     | 14.54    | 10.13 | 159.71     | 125.66     | 142.69     | 0.69       | 0.80       | 0.75       |
| Scenario #2 | Midjourney v6.1 | 0.78     | 1.00 | 0.89  | 0.63     | 0.93  | 0.78  | 63.34    | 86.76     | 75.05 | 5.88     | 10.97    | 8.43  | 122.19     | 144.28     | 133.24     | 0.81       | 0.85       | 0.83       |
|             | SD 3            | 1.00     | 1.00 | 1.00  | 0.61     | 0.75  | 0.68  | 65.08    | 83.20     | 74.14 | 6.63     | 12.69    | 9.66  | 136.57     | 158.29     | 147.42     | 0.78       | 0.80       | 0.79       |
|             | Avg.            | 0.76     | 0.82 | 0.79  | 0.44     | 0.62  | 0.53  | 62.69    | 84.39     | 73.54 | 7.04     | 13.27    | 10.16 | 147.07     | 151.86     | 149.47     | 0.77       | 0.81       | 0.79       |

TABLE 2: The effect of different p and k selections on toxicity, similarity, and execution time.

|         | Toxicity   | Toxicity   | Toxicity   | Similarity   | Similarity   | Similarity   | Similarity   | Similarity   | Similarity   | Time (s)   | Time (s)   | Time (s)   |
|---------|------------|------------|------------|--------------|--------------|--------------|--------------|--------------|--------------|------------|------------|------------|
| k Value | p =2       | p =3       | p =5       | p =2         | FID p =3     | p =5         | p =2         | CS p =3      | p =5         | p =2       | p =3       | p =5       |
| k =1    | 71.34      | 73.63      | 74.83      | 165.83       | 177.91       | 182.63       | 0.70         | 0.72         | 0.75         | 0.14       | 1.22       | 113.06     |
| k =3    | 72.53      | 73.57      | 75.21      | 173.27       | 138.36       | 187.86       | 0.75         | 0.79         | 0.78         | 0.14       | 1.23       | 112.87     |
| k =10   | 71.55      | 74.20      | 73.94      | 148.73       | 135.26       | 155.64       | 0.76         | 0.80         | 0.79         | 0.16       | 1.23       | 113.82     |

<!-- image -->

<!-- image -->

jailbreak prompts generated. A larger p increases the time required under Constraint #2 and results in generating more prompts, with a computational complexity of O ( N 5 ) . Meanwhile, k influences the number of final jailbreak prompts selected. A larger k increases the number of selections, with a computational complexity of O (1) . While adjusting k does not affect overall computational efficiency, it might impact the effectiveness of the attack. Thus, by exploring different values for p and k , we aim to balance the trade-off between attack effectiveness and computational efficiency. Table 2 provides the detailed results with p being equal to 2, 3, and 5, as well as k being equal to 1, 3, and 10.

(b)

Scenario #2

Figure 7: The effect of different p and k selections on BPR and ASR under two scenarios.

capability in generating gore images. Regarding similarity, the average FID is 122.34, and CS is 0.83 for explicit, while 119.77 and 0.76 for gore. These scores indicate that the generated images maintain semantic alignment with the intended prompts.

In Scenario #2 , MODX maintains a high average BPR of 0.76 for explicit and 0.82 for gore content. ASR remains solid, reaching 0.44 for explicit and 0.62 for gore. These BPR and ASR results indicate that MODX effectively bypasses filters to generate NSFW images containing sensitive subjects. For toxicity, the generated explicit images have a mean of 62.69 with a standard deviation of 7.04, while gore images have a mean of 84.39 with a standard deviation of 13.27, closely matching the results from Scenario #1 . This consistency demonstrates MODX's strong and stable ability to produce high-toxicity NSFW content. The average FID and CS for both categories are 149.47 and 0.79, further confirming our method's ability to maintain semantic consistency.

Trade-off . When constructing jailbreak prompts, p and k serve as adjustable hyperparameters. Selecting appropriate values for p and k can significantly enhance computational efficiency while ensuring the effectiveness of the attack. The value of p affects both the time and the number of potential

Overall, across different values of p and k , the jailbreak prompts generated by MODX achieve successful jailbreaking, showing slight variations in effectiveness but substantial differences in execution time. Figure 7 illustrates the effectiveness in terms of average BPR and ASR, and Table 2 displays the average toxicity, similarity, and execution time. When k =1 and p =2, the BPR and ASR values are the lowest across both scenarios, indicating a degree of randomness when only a single jailbreak prompt is selected. As p increases, the number of possible modifier combinations increases, leading to improvements in both BPR and ASR. With k =3, the increased selection of jailbreak prompts raises the likelihood of reaching a global optimum, resulting in noticeable improvements in BPR and ASR. The results at p =2 are lower, while those at p =3 and p =5 are both high and nearly identical, suggesting that an excessive number of combinations does not yield a significant increase in effectiveness. At k =10, there is an improvement in BPR and ASR for p =2 compared to other k values. However, for p =3 and p =5, the results are similar to those at k =3, indicating limited advantage.

Moreover, based on the results in Table 2, we observe no significant differences in toxicity or semantic similarity across different values of k and p , but execution time varies substantially. This aligns with our analysis, as increasing p exponentially impacts computational efficiency. With p =2, the time required is around 0.1 seconds; for p =3, it increases to about 1.2 seconds; and for p =5, it exceeds 110 seconds. Considering the BPR and ASR in Figure 7, where p =3 and p =5 yield similar results, we conclude that p =3 provides a balance of effectiveness and efficiency. Additionally, setting k =3 increases the likelihood of a local optimum matching the global optimum while reducing model query frequency. Thus, we select k =3 and p =3 as the optimal settings for

TABLE 3: The effect of different modifier categories on jailbreaking regarding BPR and ASR.

| Scenario    | Categories                             | BPR                 | BPR                      | ASR                           | ASR                      |
|-------------|----------------------------------------|---------------------|--------------------------|-------------------------------|--------------------------|
|             |                                        | Explicit            | Gore                     | Explicit                      | Gore                     |
| Scenario #1 | artist medium movement flavor trending | 0.76 0.92 0.90 0.92 | 0.82 0.93 0.91 0.85 0.91 | 0.53 0.23 0.28 0.46 0.21 0.68 | 0.56 0.32 0.34 0.52 0.19 |
| Scenario #1 |                                        | 0.99                |                          |                               |                          |
| Scenario #1 | ALL                                    | 0.89                | 0.94                     |                               | 0.78                     |
| Scenario #2 | artist                                 | 0.68                | 0.71                     | 0.16                          | 0.21                     |
| Scenario #2 | medium                                 | 0.87                | 0.82                     | 0.11                          | 0.13                     |
| Scenario #2 | movement                               | 0.89                | 0.91                     | 0.12                          | 0.10                     |
| Scenario #2 | flavor                                 | 0.73                | 0.72                     | 0.35                          | 0.42                     |
| Scenario #2 | trending                               | 0.85                | 0.86                     | 0.24                          | 0.29                     |
| Scenario #2 | ALL                                    | 0.75                | 0.81                     | 0.45                          | 0.60                     |

MODX in subsequent evaluations.

Ablation study . To better understand the impact of each modifier category on the effectiveness of the jailbreaking attack, we configure MODX to select only one modifier category at a time when constructing the jailbreak prompt. For each category, we choose the top three ranked modifiers, constructing a separate jailbreak prompt for each. Each model is queried four times, and the average result is recorded. Table 3 presents the experimental results. Overall, using the combination of all modifier categories has the highest ASR on explicit and gore under both scenarios.

In Scenario #1 , the subjects are safe, so BPR reflects each modifier category's ability to bypass filters. For explicit, all modifier categories achieve a BPR above 0.9, except for 'artist', which has a BPR of 0.76; for gore, all categories reach around 0.9, showing excellent performance. When using the combination, the BPR is 0.89 for explicit and 0.94 for gore. Interestingly, combining modifiers slightly increases the BPR compared to using certain individual category. Based on our theoretical analysis (Section 6), we attribute this to the upper limit of modifiers' impact on image generation, where some information is selectively ignored, resulting in certain modifier categories being less effective. Regarding ASR, the combined use of modifiers achieves the highest values of 0.68 and 0.78 for explicit and gore, respectively. Using 'artist' alone also performs well, with ASR of 0.53 and 0.56, followed by 'flavor' at around 0.5. Other modifier categories only reach around 0.2. Thus, in Scenario #1 , using the combination of modifiers is the most effective, but 'artist' and 'flavor' provide significant support for jailbreaking as well.

In Scenario #2 , the substitution subjects may not bypass the pre-filter, resulting in a slight decrease in overall BPR, but the trend remains similar to Scenario #1 . For ASR, using five combined modifier categories again yields the highest values, reaching 0.45 for explicit and 0.60 for gore. Using 'flavor' alone achieves comparable performance, with ASR of 0.35 and 0.42, respectively. The impact of 'trending' increases ASR to 0.24 and 0.29, but 'artist' is less effective than in the previous scenario. 'Medium' and 'movement' categories still have low ASR of around 0.1 in both NSFW categories when used individually. Thus, in the second

TABLE 4: Comparison of toxcity and similarity

| Method              | Category      | Toxicity    | Toxicity    | Similarity    | Similarity   |
|---------------------|---------------|-------------|-------------|---------------|--------------|
|                     |               | Mean        | Std         | FID           | CS           |
| Hateful Meme Attack | Explicit Gore | 53.34 62.94 | 17.83 19.87 | 203.89 196.83 | 0.67 0.70    |
| SneakyPrompt        | Explicit Gore | 52.73 61.85 | 14.99 17.23 | 198.73 177.99 | 0.71 0.70    |
| SurrogatePrompt     | Explicit Gore | 54.97 65.56 | 9.98 16.98  | 144.31 153.21 | 0.72 0.73    |
| MODX (Ours)         | Explicit Gore | 62.34 85.27 | 8.01 11.93  | 110.74 99.28  | 0.79 0.82    |

scenario, using the combination of modifiers provides the best attack performance, but 'flavor' and 'trending' are also helpful for jailbreaking.

Takeaway . MODX demonstrates superior performance to jailbreak state-of-the-art text-to-image models, successfully bypassing built-in filters and generating NSFW images with high toxicity and semantic similarity. Using smaller values for hyperparameters can significantly enhance the efficiency of constructing jailbreak prompts while maintaining their effectiveness. Moreover, the combination of all the modifier categories yields the best jailbreaking performance.

## 7.3. RQ2: Comparison with Baselines

In RQ2, we compare the performance of MODX with three existing studies in attack Scenario #2 . We do not include comparisons in Scenario #1 to avoid unfairness as these baselines do not consider attacks using benign subjects. Figure 8 illustrates the results in terms of BPR and ASR, and Table 4 shows the performance regarding toxicity and similarity. Overall, our method presents the highest BPR and ASR; its generated images exhibit the strongest toxicity, and the closest similarity to intended NSFW images. We provide detailed analyses from explicit and gore categories respectively as follows.

Explicit . Figure 8.(a) presents the comparison on explicit content. For BPR, all methods has a bypass rate of 1.00 on SD 3, as it does not reject generation. Beyond this, MODX demonstrates the highest bypass rate across each model, outperforming other methods. For example, on DALL · E 3, MODX achieves a BPR of 0.69, while the other three methods reach only 0.19, 0.18, and 0.25, respectively. The advantage of MODX is even more pronounced in ASR, significantly exceeding baseline methods. MODX achieves ASRs of 0.37, 0.18, 0.61, and 0.62 on DALL · E 3, Imagen 3, Midjourney v6.1, and SD 3, while the best ASR among the other three methods is only 0.08, 0.09, 0.19, and 0.18, respectively. Notably, when BPR is high (such as on SD 3 or MODX and SurrogatePrompt on Midjourney v6.1), MODX maintains an ASR exceeding 0.6, whereas other methods remain below 0.2. This highlights the reliability of MODX in jailbreaking. According to Table 4, the explicit images generated by MODX exhibit the highest toxicity,

TABLE 5: The scalability of MODX on jailbreaking against three additional NSFW categories.

| Models          | BPR   | BPR   | BPR   | ASR   | ASR   | ASR   | Toxicity   | Toxicity   | Toxicity   | Toxicity   | Toxicity   | Toxicity   | Similarity   | Similarity   | Similarity   | Similarity   | Similarity   | Similarity   |
|-----------------|-------|-------|-------|-------|-------|-------|------------|------------|------------|------------|------------|------------|--------------|--------------|--------------|--------------|--------------|--------------|
| Models          | Dis.  | Hate. | Pol.  | Dis.  | Hate. | Pol.  | Mean       | Mean       |            |            | Std        | Std        | FID          | FID          |              |              | CS           | CS           |
| Models          | Dis.  | Hate. | Pol.  | Dis.  | Hate. |       | Dis.       | Hate.      | Pol.       | Dis.       | Hate.      | Pol.       | Dis.         | Hate.        | Pol.         | Dis.         | Hateful      | Pol.         |
| DALL · E 3      | 0.98  | 0.95  | 0.93  | 0.72  | 0.68  | 0.72  | 67.23      | 72.39      | 70.11      | 10.31      | 11.92      | 8.93       | 110.92       | 128.78       | 119.24       | 0.76         | 0.78         | 0.74         |
| Imagen 3        | 0.58  | 0.59  | 0.21  | 0.48  | 0.47  | 0.18  | 75.27      | 71.12      | 80.10      | 9.37       | 14.32      | 10.93      | 131.93       | 126.61       | 180.80       | 0.71         | 0.72         | 0.69         |
| Midjourney v6.1 | 1.00  | 1.00  | 1.00  | 0.78  | 0.83  | 0.91  | 68.52      | 77.32      | 71.94      | 10.92      | 12.94      | 9.75       | 134.78       | 155.75       | 102.38       | 0.70         | 0.67         | 0.75         |
| SD 3            | 1.00  | 1.00  | 1.00  | 0.75  | 0.80  | 0.78  | 70.83      | 70.10      | 69.38      | 16.90      | 12.41      | 11.39      | 210.74       | 187.52       | 120.44       | 0.65         | 0.67         | 0.68         |
| Avg.            | 0.89  | 0.89  | 0.79  | 0.68  | 0.70  | 0.65  | 70.46      | 72.73      | 72.88      | 11.88      | 12.90      | 10.25      | 147.09       | 149.67       | 130.72       | 0.71         | 0.71         | 0.72         |

Figure 8: Comparison of existing methods and ours on BPR and ASR across four text-to-image models.

<!-- image -->

<!-- image -->

with a mean of 62.34, while other methods barely exceed 50. Additionally, our method achieves the lowest toxicity standard deviation at 8.01, indicating stable toxicity levels. In terms of similarity, it has the lowest FID and highest CS, demonstrating strong alignment with the intended NSFW images. The other three methods show higher FID and lower CS compared to MODX.

Gore . Based on Figure 8.(b), the results follow a similar trend, but with generally higher BPR and ASR. MODX maintains the highest BPR across all four models, though baseline methods are closer in comparison. However, for ASR, MODX significantly outperforms the other methods. For instance, on Midjourney v6.1, MODX achieves an ASR of 0.89, while the other methods reach only 0.08, 0.29, and 0.39. Table 4 shows that the gore images generated by our method exhibit high and stable toxicity, with a mean of 85.27 and a standard deviation of 11.93, far exceeding the baseline methods. The lowest FID and highest CS further confirm that the generated gore images maintain semantic consistency.

Takeaway . Compared to existing methods, MODX achieves the best performance, significantly surpassing others in both BPR and ASR. Additionally, the generated images exhibit a higher level of toxicity and maintain stronger semantic similarity with the original malicious prompts.

## 7.4. RQ3: Scalability and Generalization

To more comprehensively evaluate MODX's scalability and generalization, we assess its effectiveness across different NSFW categories and text-to-image models.

Scalability . We focus on Scenario #2 because hateful and political subjects are often associated with specific individuals and events, which are categorized as NSFW content. Table 5 demonstrates MODX's scalability by generating disturbing, hateful, and political images. The results show that MODX successfully generates these three NSFW categories across four models, consistently producing images with high and stable toxicity. Additionally, the generated images maintain strong semantic similarity to the intended images.

Generalization . Table 6 demonstrates MODX's generalization by attacking a broader range of mainstream models and versions. The results indicate that in both Scenario #1 and Scenario #2 , MODX successfully achieves jailbreaking with an ASR around 0.70. The generated images consistently exhibit high toxicity levels and maintain semantic similarity.

Takeaway . MODX is highly scalable, as it successfully performs attacks across five typical NSFW categories. It also exhibits strong generalization, achieving effective jailbreaking across seven mainstream models and various versions. These further highlight MODX's capability to exploit vulnerabilities of built-in filters.

## 7.5. Discussion

Reusability . MODX demonstrates exceptional performance not only in terms of effectiveness, scalability, and generalization, but also in reusability. In both attack scenarios, MODX requires only a one-time calculation per NSFW category, after which the selected modifiers can be systematically combined based on templates for repeated use. By substituting the subject, it is possible to generate diverse NSFW images in a short time, significantly enhancing efficiency.

Model vulnerabilities . Experimental results reveal that all models used in our study are vulnerable to MODX's jailbreaking, though the susceptibility varies. In generating gore images, Midjourney proves to be the most susceptible, while Imagen demonstrates the strongest resistance. Compared to gore-category NSFW images, the models exhibit greater difficulty in generating explicit content, with the average success rate (ASR) dropping by approximately 0.2, and Imagen again showing the highest resistance.

TABLE 6: The generalization of MODX in terms of jailbreaking across six additional models or versions.

| Models        | BPR      | BPR     | ASR      | ASR     | Toxicity   | Toxicity   | Toxicity   | Toxicity   | Similarity   | Similarity   | Similarity   | Similarity   |
|---------------|----------|---------|----------|---------|------------|------------|------------|------------|--------------|--------------|--------------|--------------|
| Models        | Explicit | Violent | Explicit | Violent | Mean       | Mean       | Std        | Std        | FID          | FID          | CS           | CS           |
| Models        |          |         |          |         | Explicit   | Violent    | Explicit   | Violent    | Explicit     | Violent      | Explicit     | Violent      |
| Craiyon v4    | 1.00     | 1.00    | 0.82     | 0.80    | 76.96      | 76.04      | 10.87      | 7.16       | 129.93       | 110.37       | 0.68         | 0.79         |
| FLUX v1       | 1.00     | 1.00    | 0.93     | 0.91    | 69.92      | 72.83      | 8.31       | 8.63       | 109.22       | 96.45        | 0.82         | 0.80         |
| DALL · E 2    | 0.89     | 0.98    | 0.87     | 0.94    | 68.54      | 79.83      | 5.12       | 7.29       | 114.10       | 121.08       | 0.80         | 0.86         |
| Imagen 2      | 0.23     | 0.45    | 0.19     | 0.42    | 68.93      | 74.21      | 10.83      | 11.64      | 111.09       | 91.92        | 0.93         | 0.83         |
| Midjourney v4 | 0.98     | 0.97    | 0.80     | 0.65    | 70.63      | 78.95      | 14.23      | 9.78       | 114.07       | 100.90       | 0.91         | 0.80         |
| SD XL         | 1.00     | 1.00    | 0.69     | 0.73    | 65.12      | 83.28      | 8.43       | 11.48      | 117.06       | 99.88        | 0.89         | 0.82         |
| Avg.          | 0.85     | 0.90    | 0.72     | 0.74    | 70.02      | 77.52      | 9.63       | 9.33       | 115.91       | 103.43       | 0.84         | 0.82         |
| Craiyon v4    | 1.00     | 1.00    | 0.78     | 0.82    | 80.12      | 79.27      | 9.34       | 8.64       | 122.66       | 121.58       | 0.71         | 0.80         |
| FLUX v1       | 1.00     | 1.00    | 0.88     | 0.79    | 77.89      | 69.97      | 10.57      | 13.62      | 118.06       | 104.81       | 0.83         | 0.81         |
| DALL · E 2    | 0.75     | 0.79    | 0.88     | 0.70    | 75.32      | 88.94      | 9.37       | 11.19      | 127.62       | 144.38       | 0.83         | 0.82         |
| Imagen 2      | 0.21     | 0.32    | 0.17     | 0.20    | 76.42      | 89.45      | 7.59       | 12.84      | 137.95       | 140.25       | 0.77         | 0.86         |
| Midjourney v4 | 0.84     | 0.89    | 0.78     | 0.69    | 72.47      | 87.36      | 9.61       | 10.87      | 105.31       | 112.94       | 0.89         | 0.84         |
| SD XL         | 1.00     | 1.00    | 0.66     | 0.68    | 70.12      | 83.74      | 10.21      | 8.99       | 129.74       | 114.81       | 0.90         | 0.85         |
| Avg.          | 0.80     | 0.81    | 0.69     | 0.64    | 75.39      | 83.12      | 9.45       | 11.02      | 123.56       | 123.13       | 0.82         | 0.83         |

Artistic expression in contrast to NSFW content . The boundary between artistic expression and NSFW content is often ambiguous. Artistic works can depict sensitive themes, but NSFW classification is determined not just by artistic genre, but also by content, context, and norms or platform policies:

TABLE 7: The ASR of MODX when negative prompt mitigation is applied.

- Content . NSFW material often reduces aesthetic quality but amplifies unsettling nature (e.g., gore and sexually explicit content).
- Context . Artistic genres have culture or historical framing, but NSFW images often prioritize explicitness over artistic interpretation.
- Regulation . Artistic genres receive legal protection in museums and other media, whereas AI-generated content falls under digital content regulations and age restrictions.

## 8. Mitigation

To strengthen defenses against modifier-based jailbreaking, multi-faceted strategies are essential. In this section, we discuss the potential mitigation measures and their challenges for MODX from the perspectives of modifier regulation, policy enforcement, and usage of negative prompts. Controls over modifiers . Implementing stricter controls over the use of modifiers can mitigate the risk of jailbreaking. Our experiments (Table 3 in Section 7.2) show that limiting the categories and combinations of modifiers can reduce the likelihood of generating NSFW content, but still maintain the artistic genre and semantic consistency. While this measure can mitigate modifier-based jailbreaking attacks to some extent, it could significantly reduce the diversity and artistic quality of generated images. Balancing these two aspects remains an area with considerable potential for further exploration.

Boundaries between unsafe and other genres . Differentiating between unsafe and other artistic genres can serve as a measure to mitigate jailbreaking. By establishing clear boundaries that classify unsafe artistic genres under the NSFW category, the filters in models can be programmed to automatically reject prompts associated with these styles.

|             | Models          | ASR under NP        | ASR under NP   | ASR under NP   | ASR Variation   | ASR Variation   | ASR Variation   |
|-------------|-----------------|---------------------|----------------|----------------|-----------------|-----------------|-----------------|
|             |                 | Explicit            | Gore           | Avg.           | Explicit        | Gore            | Avg.            |
| Scenario #1 | DALL·E 3        | 0.50 0.41 0.54 0.46 | 0.53           | 0.52           | -0.25           | -0.37           | -0.31           |
| Scenario #1 | Imagen 3        |                     | 0.59           | 0.50           | -0.23           | -0.17           | -0.20           |
| Scenario #1 | Midjourney v6.1 |                     | 0.71           | 0.63           | -0.15           | -0.13           | -0.14           |
| Scenario #1 | SD 3            |                     | 0.48           | 0.47           | -0.14           | -0.17           | -0.16           |
| Scenario #1 | Avg.            | 0.48                | 0.58           | 0.53           | -0.19           | -0.21           | -0.20           |
| Scenario #2 | DALL·E 3        | 0.21                | 0.37           | 0.29           | -0.14           | -0.18           | -0.16           |
| Scenario #2 | Imagen 3        | 0.09                | 0.17           | 0.13           | -0.07           | -0.07           | -0.07           |
| Scenario #2 | Midjourney v6.1 | 0.45                | 0.74           | 0.60           | -0.18           | -0.19           | -0.19           |
| Scenario #2 | SD 3            | 0.40                | 0.58           | 0.49           | -0.21           | -0.17           | -0.19           |
| Scenario #2 | Avg.            | 0.29                | 0.47           | 0.38           | -0.15           | -0.15           | -0.15           |

Such a measure requires a well-defined taxonomy of artistic genres, with a particular emphasis on identifying styles that can be exploited to bypass safety filters. Implementing this in practice is challenging due to the difficulty in defining clear, universally applicable boundaries for unsafe artistic genres, balancing safety with creative freedom, and the need for continuous updates to address emerging artistic genres. Negative prompts . The negative prompt (NP) is an implicit mechanism specifying elements that should not appear in generated images. It suppresses features associated with NSFW content in the latent space, and thus can be used for guiding text-to-image models not to generate NSFW elements during the denoising process. Service providers can expand negative prompts to include a set of NSFW-related descriptions.

We conduct experiments to explore the effectiveness of using negative prompts to mitigate MODX jailbreaking. Based on the crafted jailbreak prompts used for NSFW image generation in Section 7, we select the top 5% most frequently occurring modifiers in MMD as negative prompts and apply them to text-to-image models. For Stable Diffusion, we directly input these modifiers into the model's built-in negative prompt option. For Midjourney, we utilize the --no command to achieve the same effect. For DALL · E and Imagen, we append the phrase ' negative prompt: ' after the input to guide the model in incorporating negative prompts.

The experimental results are presented in Table 7. Over-

all, using negative prompts results in a reduction in MODX's ASR across all four models in both scenarios. For instance, in Scenario #1 , the average ASR for the explicit and gore categories decreases from 0.83 to 0.52 on DALL · E 3, with the gore category exhibiting the most significant drop of 0.37. Similar reductions are observed for Imagen 3, Midjourney v6.1, and Stable Diffusion 3. In Scenario #2 , the results remain consistent within Scenario #1 , showing an average ASR reduction of 0.15 across the four models. These findings demonstrate the effectiveness of negative prompts as a mitigation strategy. Although this is a practical mitigation, identifying negative prompts that effectively cover all NSFW categories remains challenging, requiring further research and greater attention from the community.

## 9. Related Work

Concerns in text-to-image models . Although text-to-image models exhibit unprecedented high-quality image-generation capabilities, researchers have expressed concerns by exposing vulnerabilities in these models from different aspects. Duan et al. [30] propose Step-wise Error Comparing Membership Inference (SecMI), a query-based MIA, to infer membership in text-to-image diffusion models by assessing the matching of forward process posterior estimation at each timestep. Vice et al. [59] introduce BAGM, a backdoor attack for text-to-image models, aiming at injecting manipulative details naturally blended into the content by altering the behavior of embedded symbol generators and image generation models. Liu et al. [39] present RIATIG, an imperceptible adversarial attack designed to make textto-image models generate images that are semantically unrelated to the original prompts. Shen et al. [57] propose a prompt stealing attack that seeks to recover the original prompt based on the model-generated images.

Jailbreaking . In addition to the aforementioned attacks, There is a special category of attacks on text-to-image models focused on generating NSFW images, i.e., jailbreaking. Jailbreaking poses severe risks to both the community and society, as the generated NSFW images can cause discomfort and hallucinate individuals by misguiding. However, only a few studies step into this domain. Qu et al. [44] utilize advanced image editing techniques to force Stable Diffusion to generate hateful memes and their variants. Yang et al. [61] propose SneakyPrompt, a framework that employs reinforcement learning to perform automatic jailbreaking attacks, bypassing DALL · E 2's safety filter to generate NSFW images. Ba et al. [24] propose SurrogaePrompt, utilizing large language models and image-to-text modules to automate jailbreak prompt creation by substituting sensitive subjects.

## 10. Conclusion

We propose MODX, a novel modifier-based jailbreak framework that induces the text-to-image models to generate NSFW images. It employs a heuristic algorithm to identify suitable jailbreak prompts from our Malicious Modifier

Dataset, adjusting the image genre to NSFW or facilitating the generation of sensitive subjects, thus achieving successful jailbreaking. We provide formal proof demonstrating the feasibility of using modifiers to bypass filters and generate NSFW images, establishing a foundation for MODX. Our experimental results indicate that MODX successfully jailbreaks state-of-the-art text-to-image models, achieving an attack success rate of up to 0.93. Additionally, its high scalability and generalization reveal shared vulnerabilities across current models' built-in filters.

## Ethical Consideration

Disclosure . Throughout our research, we utilize anonymous and publicly available datasets and images, and there is no risk related to user de-anonymization. Therefore, our work does not involve personally identifiable information and is not considered human subjects research by the Institutional Review Board (IRB). As our study aims to analyze and expose vulnerabilities and security issues in text-to-image models, some prompts contain unsafe text and generate NSFW images. To minimize risks and prevent potential misuse, all research activities are conducted exclusively by the authors of this study without third-party involvement. Additionally, we release our MMD with controlled access restrictions and commit to not sharing our prompts and NSFW images with any third parties without explicit institutional approval and legal guidance.

Support for researchers . To ensure the well-being of authors, safeguards are implemented to protect them psychologically, physically, and ethically throughout the entire research process.

- Prior to engaging in the NSFW content generation, all authors undergo psychological briefing to prepare for the potential mental and physical impact.
- During the research, an inquiry and feedback mechanism is established to monitor their psychological states. Accordingly, they apply rotational breaks and adjust task assignments.
- Upon completion of the study, all authors participate in a psychological assessment and debriefing to ensure their well-being.

Inclusion of NSFW contents in this paper . To prevent potential offense, we minimize the inclusion of NSFW images in the paper, and include them only when necessary. They are listed to directly illustrate the severity (Figure 1) and effectiveness (Figure 4) of the modifier-based jailbreaking, and to provide an intuitive explanation of our methodology (Figure 6). Additionally, we blur the sexually explicit images, selectively present gore-related images, and avoid displaying images in other NSFW categories.

Prevention of abuse . As MODX might be unintentionally or maliciously used, we have implemented strategies to reduce its impact. First, the full attack code, as well as the generated malicious prompts and NSFW images will not be publicly released or shared. We release MMD with controlled access authorization by verifying applicant identities and intended

use. Second, we provide possible mitigation strategies (Section 8) to reduce the misuse of MODX. Third, to ensure responsible disclosure, we have proactively reported our findings to the providers of models we have tested, through email correspondences or their bug tracker platforms. We have received responses from OpenAI and Google, who both acknowledge the vulnerabilities identified in our research.

## Acknowledgments

We appreciate our shepherd and anonymous reviewers for their insightful comments from IEEE S&amp;P 2025 to improve this manuscript. This work is partially supported by Australian Research Council (ARC) Discovery Projects (DP230101196, DP240103068). Minhui Xue is supported in part by ARC DP240103068 and in part by CSIRO - National Science Foundation (US) AI Research Collaboration Program.

## References

| [1]   | 4chan. https://www.4chan.org/index.php.                                                                                                             |
|-------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| [2]   | Clip interrogator. https://github.com/pharmapsychotic/clip- interrogator.                                                                           |
| [3]   | Craiyon. https://www.craiyon.com.                                                                                                                   |
| [4]   | Dalle content policy. https://help.openai.com/en/articles/6338764- are-there-any-restrictions-to-how-i-can-use-dall-e-2-is-there-a- content-policy. |
| [5]   | Dark art movement. https://darkartmovement.com/dark-art- movement.                                                                                  |
| [6]   | Deviant art. https://www.deviantart.com.                                                                                                            |
| [7]   | Flux. https://flux-ai.io/flux-ai-image-generator.                                                                                                   |
| [8]   | Generative ai prohibited use policy. https://policies.google.com/terms/ generative-ai/use-policy.                                                   |
| [9]   | google. https://www.google.com.                                                                                                                     |
| [10]  | Gpt-4o. https://openai.com/index/hello-gpt-4o.                                                                                                      |
| [11]  | Imagen 3 our highest quality text-to-image model. https://deepmind. google/technologies/imagen-3.                                                   |
| [12]  | Malicious modifier dataset (mmd). https://huggingface.co/datasets/ cola-hunter/Malicious Modifier Dataset MMD.                                      |
| [13]  | Midjourney. https://www.midjourney.com/home.                                                                                                        |
| [14]  | New models and developer products announced at devday. https://openai.com/index/new-models-and-developer-products- announced-at-devday.             |
| [15]  | Nsfwpromptshare. https://www.reddit.com/r/NSFWPromptShare.                                                                                          |
| [16]  | Openai. https://openai.com.                                                                                                                         |
| [17]  | Prompt engineering. https://github.com/benrugg/AI-Render/wiki/ Prompt-Engineering.                                                                  |
| [18]  | Prompthero. https://prompthero.com.                                                                                                                 |
| [19]  | reddit. https://www.reddit.com.                                                                                                                     |
| [20]  | Saatchi art. https://www.saatchiart.com.                                                                                                            |
| [21]  | stability.ai. https://stability.ai.                                                                                                                 |
| [22]  | Taylor swift deepfakes spark calls in congress for new legislation. https://www.bbc.com/news/technology-68110476.                                   |

- [23] Verified twitter accounts share fake image of explosion near pentagon, causing confusion. https://www.cnn.com/2023/05/22/tech/ twitter-fake-image-pentagon-explosion/index.html.
- [24] Zhongjie Ba, Jieming Zhong, Jiachen Lei, Peng Cheng, Qinglong Wang, Zhan Qin, Zhibo Wang, and Kui Ren. Surrogateprompt: Bypassing the safety filter of text-to-image models via substitution. In Proceedings of the 2024 ACM SIGSAC Conference on Computer and Communications Security (CCS) , 2024.
- [25] Stephen Bach, Victor Sanh, Zheng Xin Yong, Albert Webson, Colin Raffel, Nihal V Nayak, Abheesht Sharma, Taewoon Kim, M Saiful Bari, Thibault Fevry, et al. Promptsource: An integrated development environment and repository for natural language prompts. In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (ACL) , pages 93-104, 2022.
- [26] Barry Becker and Ronny Kohavi. Adult. UCI Machine Learning Repository, 1996. DOI: https://doi.org/10.24432/C5XW20.
- [27] Gelei Deng, Yi Liu, Yuekang Li, Kailong Wang, Ying Zhang, Zefeng Li, Haoyu Wang, Tianwei Zhang, and Yang Liu. Masterkey: Automated jailbreaking of large language model chatbots. In Proceedings of the 2024 Network and Distributed System Security Symposium (NDSS) , 2024.
- [28] Yimo Deng and Huangxun Chen. Divide-and-conquer attack: Harnessing the power of llm to bypass the censorship of text-to-image generation model. CoRR abs/2312.07130 , 2023.
- [29] Prafulla Dhariwal and Alexander Nichol. Diffusion models beat gans on image synthesis. In Advances in Neural Information Processing Systems (NeurIPS) , 2021.
- [30] Jinhao Duan, Fei Kong, Shiqi Wang, Xiaoshuang Shi, and Kaidi Xu. Are diffusion models vulnerable to membership inference attacks? In Proceedings of the 40th International Conference on Machine Learning (ICML) , pages 8717-8730. PMLR, 2023.
- [31] Patrick Esser, Sumith Kulal, Andreas Blattmann, Rahim Entezari, Jonas M¨ uller, Harry Saini, Yam Levi, Dominik Lorenz, Axel Sauer, Frederic Boesel, et al. Scaling rectified flow transformers for highresolution image synthesis. In Proceedings of the 41st International Conference on Machine Learning (ICML) , 2024.
- [32] Yingchaojie Feng, Xingbo Wang, Kam Kwai Wong, Sijia Wang, Yuhong Lu, Minfeng Zhu, Baicheng Wang, and Wei Chen. Promptmagician: Interactive prompt engineering for text-to-image creation. IEEE Transactions on Visualization and Computer Graphics (TVCG) , 2023.
- [33] Rohit Gandikota, Joanna Materzynska, Jaden Fiotto-Kaufman, and David Bau. Erasing concepts from diffusion models. In Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV) , pages 2426-2436, 2023.
- [34] Yaru Hao, Zewen Chi, Li Dong, and Furu Wei. Optimizing prompts for text-to-image generation. In Advances in Neural Information Processing Systems (NeurIPS) , 2024.
- [35] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. In Advances in Neural Information Processing Systems (NeurIPS) , 2020.
- [36] Alex Krizhevsky. Learning multiple layers of features from tiny images. 2009.
- [37] Xinfeng Li, Yuchen Yang, Jiangyi Deng, Chen Yan, Yanjiao Chen, Xiaoyu Ji, and Wenyuan Xu. SafeGen: Mitigating Sexually Explicit Content Generation in Text-to-Image Models. In Proceedings of the 2024 ACM SIGSAC Conference on Computer and Communications Security (CCS) , 2024.
- [38] Chumeng Liang, Xiaoyu Wu, Yang Hua, Jiaru Zhang, Yiming Xue, Tao Song, Zhengui Xue, Ruhui Ma, and Haibing Guan. Adversarial example does good: Preventing painting imitation from diffusion models via adversarial examples. In Proceedings of the 40th International Conference on Machine Learning (ICML) , pages 20763-20786. PMLR, 2023.

| [39]   | Han Liu, Yuhao Wu, Shixuan Zhai, Bo Yuan, and Ning Zhang. Riatig: Reliable and imperceptible adversarial text-to-image generation with natural prompts. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) , pages 20585- 20594, 2023.                                                                 |
|--------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [40]   | Shuofeng Liu, Zihan Wang, Minhui Xue, Long Wang, Yuanchao Zhang, and Guangdong Bai. Being transparent is merely the begin- ning: enforcing purpose limitation with polynomial approximation. In 33rd USENIX Security Symposium (USENIX Security) , pages 6507- 6524, 2024.                                                                      |
| [41]   | Vivian Liu and Lydia B Chilton. Design guidelines for prompt engineering text-to-image generative models. In Proceedings of the 2022 Conference on Human Factors in Computing Systems (CHI) , pages 1-23, 2022.                                                                                                                                 |
| [42]   | Mengyao Ma, Shuofeng Liu, MAP Chamikara, Mohan Baruwal Chhetri, and Guangdong Bai. Unveiling intellectual property vulnerabilities of gan-based distributed machine learning through model extraction attacks. In Proceedings of the 33rd ACM International Conference on Information and Knowledge Management (CIKM) , pages 1617-1626, 2024.  |
| [43]   | Jonas Oppenlaender. A taxonomy of prompt modifiers for text-to- image generation. Behaviour & Information Technology , pages 1-14, 2023.                                                                                                                                                                                                        |
| [44]   | Yiting Qu, Xinyue Shen, Xinlei He, Michael Backes, Savvas Zan- nettou, and Yang Zhang. Unsafe diffusion: On the generation of unsafe images and hateful memes from text-to-image models. In Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security (CCS) , pages 3403-3417, 2023.                                |
| [45]   | Yiting Qu, Xinyue Shen, Yixin Wu, Michael Backes, Savvas Zannet- tou, and Yang Zhang. Unsafebench: Benchmarking image safety clas- sifiers on real-world and ai-generated images. CoRR abs/2405.03486 , 2024.                                                                                                                                   |
| [46]   | Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language supervision. In Proceedings of the 38th International Conference on Machine Learning (ICML) , pages 8748-8763. PMLR, 2021. |
| [47]   | Aditya Ramesh, Prafulla Dhariwal, Alex Nichol, Casey Chu, and Mark Chen. Hierarchical text-conditional image generation with clip latents. CoRR abs/2204.06125 , 2022.                                                                                                                                                                          |
| [48]   | Aditya Ramesh, Mikhail Pavlov, Gabriel Goh, Scott Gray, Chelsea Voss, Alec Radford, Mark Chen, and Ilya Sutskever. Zero-shot text- to-image generation. In n Proceedings of the 38th International Conference on Machine Learning (ICML) , pages 8821-8831. Pmlr, 2021.                                                                         |
| [49]   | Javier Rando, Daniel Paleka, David Lindner, Lennart Heim, and Florian Tramer. Red-teaming the stable diffusion safety filter. In The 2022 NeurIPS Workshop on Machine Learning Safety , 2022.                                                                                                                                                   |
| [50]   | Nils Reimers and Iryna Gurevych. Sentence-bert: Sentence em- beddings using siamese bert-networks. In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP) , 2019.                                                                                                                                    |
| [51]   | Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Bj¨ orn Ommer. High-resolution image synthesis with latent diffusion models. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) , pages 10684- 10695, 2022.                                                                       |
| [52]   | Chitwan Saharia, William Chan, Saurabh Saxena, Lala Li, Jay Whang, Emily L Denton, Kamyar Ghasemipour, Raphael Gontijo Lopes, Burcu Karagol Ayan, Tim Salimans, et al. Photorealistic text-to-image diffusion models with deep language understanding. In Advances in Neural Information Processing Systems (NeurIPS) , 2022.                   |

| [53]   | Patrick Schramowski, Manuel Brack, Bj¨ orn Deiseroth, and Kristian Kersting. Safe latent diffusion: Mitigating inappropriate degeneration in diffusion models. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) , pages 22522- 22531, 2023.                  |
|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [54]   | Patrick Schramowski, Christopher Tauchmann, and Kristian Kersting. Can machines help us answering question 16 in datasheets, and in turn reflecting on inappropriate content? In Proceedings of the 2022 ACM Conference on Fairness, Accountability, and Transparency (FAccT) , pages 1350-1361, 2022.  |
| [55]   | Erfan Shayegani, Yue Dong, and Nael Abu-Ghazaleh. Jailbreak in pieces: Compositional adversarial attacks on multi-modal language models. In Proceedings of the 12th International Conference on Learning Representations (ICLR) , 2023.                                                                 |
| [56]   | Xinyue Shen, Zeyuan Chen, Michael Backes, Yun Shen, and Yang Zhang. 'do anything now': Characterizing and evaluating in-the-wild jailbreak prompts on large language models. In Proceedings of the 2024 on ACM SIGSAC Conference on Computer and Communications Security (CCS) , pages 1671-1685, 2024. |
| [57]   | Xinyue Shen, Yiting Qu, Michael Backes, and Yang Zhang. Prompt stealing attacks against { Text-to-Image } generation models. In 33rd USENIX Security Symposium (USENIX Security) , pages 5823-5840, 2024.                                                                                               |
| [58]   | Jascha Sohl-Dickstein, Eric Weiss, Niru Maheswaranathan, and Surya Ganguli. Deep unsupervised learning using nonequilibrium thermo- dynamics. In Proceedings of the 32rd International Conference on Machine Learning (ICML) , pages 2256-2265. PMLR, 2015.                                             |
| [59]   | Jordan Vice, Naveed Akhtar, Richard Hartley, and Ajmal Mian. Bagm: A backdoor attack for manipulating text-to-image generative models. IEEE Transactions on Information Forensics and Security (TIFS) , 2024.                                                                                           |
| [60]   | Jiaqi Wang, Zhengliang Liu, Lin Zhao, Zihao Wu, Chong Ma, Sigang Yu, Haixing Dai, Qiushi Yang, Yiheng Liu, Songyao Zhang, et al. Review of large vision models and visual prompt engineering. Meta- Radiology , page 100047, 2023.                                                                      |
| [61]   | Yuchen Yang, Bo Hui, Haolin Yuan, Neil Gong, and Yinzhi Cao. Sneakyprompt: Jailbreaking text-to-image generative models. In Proceedings of the IEEE Symposium on Security and Privacy (S&P) , pages 897-912, 2024.                                                                                      |
| [62]   | Yuxin Zhang, Nisha Huang, Fan Tang, Haibin Huang, Chongyang Ma, Weiming Dong, and Changsheng Xu. Inversion-based style transfer with diffusion models. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) , pages 10146- 10156, 2023.                          |

## Appendix A.

## Workflow of Diffusion Models

A typical diffusion-based text-to-image pipeline involves a text encoder that translates the input prompt into a latent representation. Given an input text prompt P , the text encoder, e.g., CLIP [46], converts P into a latent representation c in a high-dimensional semantic space, i.e., c = E ( P ) , where E is the text encoder. c ∈ R d (where d is the dimension of the embedding) represents the semantic embedding of the prompt, which serves as the conditioning input for the diffusion process guiding the denoising steps. During the denoising steps, the model starts with a randomly initialized noise image x T ∼ N (0 , I ) , and then iteratively denoises x t through T steps down to x 0 , where each denoising step is conditioned on both the previous noisy image x t and c .

## Appendix B.

## Modifier Collection on Three Online Platforms

For art-related websites, we focus on the following three platforms. We explain the procedures for modifier collection on them as follows.

- DeviantArt [6]. As the largest online art gallery and community, DeviantArt features various artistic forms, artists, and styles, divided into 16 categories. We review the top 50 artworks in each category, use Q16 [54] to check for NSFW content, and record the modifiers from the tags of images that are classified as NSFW.
- Saatchi Art [20]. A renowned platform for selling drawings, providing detailed descriptions of artworks. We search for NSFW-related artworks and record the modifiers from their tags.
- Dark Art Movement [5]. This website is filled with dark art. We collect the modifiers from their tags.

## Appendix C. CLIP Interrogator's Taxonomy of Modifiers

The modifiers are classified into 5 categories by CLIP Interrogator. Table 8 provides the descriptions and examples for each category.

TABLE 8: Modifier categorization by CLIP Interrogator

| Category                               | Description                                                                                                                                                                                                                          | Example                                              |
|----------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------|
| artist medium movement flavor trending | the style or influence of a specific artist the type of artistic medium used in visual art the artistic movement or styles of visual art specific stylistic or thematic details current trends or popular styles on social platforms | Picasso watercolor impressionism thriller artstation |

## Appendix D. Case Study of MODX on Gore category

We provide a detailed explanation of generating gore images using MODX.

Scenario #1 . Using MODX, we generate gore images with common objects as the subject. We choose 'a dog' as the original prompt and ask GPT-4 to produce two synonyms for 'gore', resulting in 'bloodshed' and 'gruesome'. Following the constraints in Constraint #1 and Constraint #2 , and setting p =2 and k =3, we ultimately obtain three jailbreak prompts to use for attacks on DALL · E 3 and SD 3. The second row in Figure 6.(a) shows the prompts and corresponding results.

Scenario #2 . We select 'blood over the body' as the malicious prompt. We use GPT-4o to get substitutions for 'blood', and we obtain 'tomato juice', 'red paint', and 'red dye'. By calculating the semantic similarity, 'red paint' is the closest. The rest processes are the same as in the first scenario. The jailbreak prompts and gore images are illustrated in the second row in Figure 6.(b).

## Appendix E. Proof of Theorems

We present our detailed theoretical proofs of theorems in this section.

## E.1. Proof of Theorem 1

Proof. According to Assumption 1, the text encoder E is considered a continuously differentiable function, so we can approximate E ( p m ) using a Taylor expansion around p o ,

<!-- formula-not-decoded -->

where ∇ p E ( p o ) is the gradient of E at p o , and O ( ∥ l ∥ 2 ) is the higher-order terms. Then we can express the difference between E ( p o ) and E ( p m ) as,

<!-- formula-not-decoded -->

Since the text encoder E is Lipschitz continuity, the gradient's variation is controlled by the Lipschitz constant within a local region and thus we have,

<!-- formula-not-decoded -->

Then, we can obtain,

<!-- formula-not-decoded -->

To satisfy the Lipschitz continuity, O ( ∥ l ∥ 2 ) is negligible, which means Eq. 14 holds. Therefore, we prove that the difference between the embeddings of the original prompt and the modified prompt with modifiers is bounded.

## E.2. Proof of Theorem 2

Proof. When adding modifiers to the original prompt, the conditioning changes from c o to c m . The difference at each denoising step can be expressed as follows according to Eq. 1,

<!-- formula-not-decoded -->

where c m = E ( p m ) and c o = E ( p o ) . According to Assumpotion 2, ϵ ( x, t, c ) is Lipschitz continuous with respect to the conditioning c with constant L , so we obtain,

<!-- formula-not-decoded -->

Therefore, based on Eq. 14 and Eq. 25, we have

<!-- formula-not-decoded -->

We substitute this bound into the difference at each denoising step, we can get

<!-- formula-not-decoded -->

The final output difference ∥ x 0 m -x 0 o ∥ is the cumulative effect of each step's difference from t = T down to t = 1 . We sum the bounds across all steps, and we finally obtain Eq. 15.

## E.3. Proof of Theorem 3

Proof. According to the triangle inequality of Wasserstein distance, we have

<!-- formula-not-decoded -->

We also know according to Assumption 3, the 1-Wasserstein distance of D b and D nsfw can be expressed as Eq. 13. Based on Theorem 2 and Definition 6, we obtain,

<!-- formula-not-decoded -->

Therefore, Eq. 16 holds.

## E.4. Proof of Theorem 4

Proof. According to Eq. 15, we can obtain,

<!-- formula-not-decoded -->

where ϵ is a small positive constant. Similarly, according to Eq. 16, we get

<!-- formula-not-decoded -->

where ϵ is a small positive constant. Practically, this condition is chosen to ensure that ∥ l ∥ 2 remains small enough. To ensure both conditions are met, we can select ∥ l ∥ 2 to satisfy the smaller of the two upper bounds, which is expressed as Eq. 17. Therefore, we can find a suitable ∥ l ∥ 2 that satisfies both Theorem 2 and Theorem 3.

## Appendix F.

## Meta-Review

The following meta-review was prepared by the program committee for the 2025 IEEE Symposium on Security and Privacy (S&amp;P) as part of the review process as detailed in the call for papers.

## F.1. Summary

This paper introduces MODX, a novel framework for jailbreaking text-to-image models by strategically using modifiers in prompts to bypass built-in safety filters and generate Not-Safe-for-Work (NSFW) content. The authors propose a heuristic algorithm with two constraints to identify modifiers that subtly introduce unsafe elements into generated images, exploiting the fact that safety filters often fail to block certain artistic styles or genres. Empirically, MODX is evaluated across four state-of-the-art text-to-image models (DALL · E 3, Midjourney, Imagen, and Stable Diffusion) and multiple NSFW categories (e.g., explicit, gore, disturbing). The results show that MODX consistently outperforms existing jailbreaking methods in terms of bypass rate (BPR) and attack success rate (ASR), demonstrating strong scalability and generalization.

## F.2. Scientific Contributions

- Provides a New Data Set for Public Use.
- Identifies an Impactful Vulnerability.
- Provides a Valuable Step Forward in an Established Field.
- Independent Confirmation of Important Results with Limited Prior Research.
- Creates a New Tool to Enable Future Science.
- Addresses a Long-Known Issue.

## F.3. Reasons for Acceptance

- Provides a Valuable Step Forward in an Established Field. This paper presents a novel modifier-based attack tailored for modern text-to-image AI models. It provides a rigorous and comprehensive evaluation of this attack, demonstrating its feasibility.
- Provides a New Data Set for Public Use. This paper produces a Malicious Modifier Dataset (MMD) which includes modifiers which correlate with the generation of NSFW images, derived from publicly available examples of NSFW images generated using text-to-image models.