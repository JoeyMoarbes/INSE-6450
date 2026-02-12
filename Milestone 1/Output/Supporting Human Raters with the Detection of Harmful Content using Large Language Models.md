## Supporting Human Raters with the Detection of Harmful Content using Large Language Models

Kurt Thomas 1 Patrick Gage Kelley 1 David Tao 1 Sarah Meiklejohn 1 Owen Vallis 1 Shunwen Tan 1 Blaˇ z Brataniˇ c 2 Felipe Tiengo Ferreira 2 Vijay Kumar Eranti 1 Elie Bursztein 1 1 Google 2 Google DeepMind

Abstract -In this paper, we explore the feasibility of leveraging large language models (LLMs) to automate or otherwise assist human raters with identifying harmful content including hate speech, harassment, violent extremism, and election misinformation. Using a dataset of 50,000 user comments, we demonstrate that LLMs can achieve 90% accuracy when compared to human verdicts. We explore how to best leverage these capabilities, proposing five design patterns that integrate LLMs with human rating, such as pre-filtering non-violative content, detecting potential errors in human rating, or surfacing critical context to support human rating. We outline how to support all of these design patterns using a single, optimized prompt. Beyond these synthetic experiments, we share how piloting our proposed techniques in a real-world review queue yielded a 41.5% improvement in optimizing available human rater capacity, and a 9-11% increase (absolute) in precision and recall for detecting violative content.

This paper includes descriptions and quotes of harmful content. We have redacted this content to minimize harm; take care of yourself when engaging with this material.

## 1. Introduction

Protecting users from abuse has expanded in its purpose-from an original focus on scams, phishing, and malware-to now encompass a spectrum of harmful content . Threats include hate and harassment that attempt to silence online voices [53]; violent extremism that glorifies terrorist attacks [10]; and misinformation and disinformation that diminishes trust in institutions (e.g., vaccines approved by the medical establishment or the integrity of fair elections) [26], [33]. In practice, robustly defining harmful content requires a multitude of specialized policies, the nuances and enforcement of which differ from platform to platform and by country or locality [50], [43], [18].

Platforms have responded to harmful content with a defense-in-depth approach. Protections include content classifiers and hash databases that detect violative content , such as Jigsaw's Perspective API [29], the GIFCT terrorist image database [12], and recent APIs from Google and Microsoft [15], [37]. User reporting serves to both surface emerging threats as well as to call attention to content

DOI 10.1109/SP61157.2025.00082

missed by detection systems [6]. And appeals serve to safeguard against non-violative content being inaccurately flagged and removed [40], [54].

Ultimately, training data and decisions for all of these systems and policies hinges on human raters who bring incontext, human expertise. This poses an ongoing challenge for a variety of reasons. Expertise is a scarce resource compared to the scale of user content generated daily. Policy clauses (and interpretations) can rapidly change in response to new product features, regulations, and emerging threats (e.g., evolution in hate speech [60]). Decisions can require regional knowledge pertaining to languages, cultures, and memes [63], [60]. Finally, exposure to harmful content incurs a burden on those involved [52]. Streamlining or improving human decision making can thus help with the scale and efficacy of protecting users from harmful content, while also ensuring more consistent and fair enforcement [34].

In this paper, we explore how to harness a sea-change moment with the emergence of large language models (LLMs) to optimize what content receives a human rater's consideration and how human raters arrive at a policy decision. Specifically, we examine:

- RQ1: What prompt engineering practices, without finetuning, maximize an LLM's ability to interpret realworld policies for multiple types of harmful content?

RQ2: What design patterns-such as filtering non-violative content, rapidly escalating violative content, or surfacing critical context to human raters-best utilize the current capabilities of LLMs?

RQ3: What is the real-world impact of deploying an LLM to assist human raters with detecting harmful content?

To answer these questions, we leverage a dataset of 40,000 text comments written in English that human raters at Google identified as violating its hate speech, harassment, violent extremism, or election misinformation policies [14]; as well as 10,000 comments that human raters determined did not violate any of Google's policies. We experiment with a variety of prompting strategies to classify each comment (e.g., retrieval augmented generation [30] and chain of thought [56]) and evaluate each prompt variant on Google's PaLM 2 text-bison and text-unicorn models [13].

We find that LLMs can achieve accurate policy decisions compared to human raters, with our best prompt on textunicorn achieving 98.7% accuracy for election misinformation, 91.1% accuracy for hate speech, 91.1% accuracy for violent extremism, and 90.1% accuracy for harassment. At the same time, we show that a single prompting strategy is flexible enough to support a variety of design patterns. These include pre-filtering likely non-violative content, rapidly escalating violative content, detecting potential errors in human ratings, and surfacing critical context to human raters.

We demonstrate the real-world feasibility of our proposed approach on a review queue at Google that covers 20+ harmful content policies. We show that just a single prompt, encompassing every policy, achieves 95.1% recall of violative content, thus allowing automated decisions for 41.5% of the queue so human raters can focus their time on borderline content-rather than clearly benign content. Furthermore, in an experiment where LLMs assist human raters with detection by highlighting relevant text passages, human rating precision and recall both increase by 9-11% (absolute). Taken as a whole, our results highlight how LLMs represent a promising direction for scaling human expertise for trust and safety, which can reduce the time to decision making, reduce burden on human raters, ensure consistency, and in some cases improve overall accuracy.

## 2. Related work

Defining and understanding harmful content. The scale and scope of policies that govern harmful content have evolved along with the global user bases of online platforms [19]. Researchers have explored some of the most pressing categories of harmful content, including hate speech and harassment [39], [49], [53], violent extremism [10], misinformation [26], [33], and child safety [4], [46]; as well as the idiosyncrasies of policies across platforms [43], [50]. Other works have looked to systematize the space according to the harms different content might incur [48] or the viability of interventions [50].

Additionally, major platforms are shifting towards greater transparency, releasing more detailed information on the specific policies they use to moderate content, partially due to requirements in the Digital Services Act (DSA) [2]; examples include the Meta Transparency Center [36] and Google Transparency Center [14]. This offers researchers better visibility into how platforms make moderation decisions, and what content is considered violative.

Detecting harmful content. Platforms and researchers have developed a plethora of detection strategies for identifying harmful content, most often in the form of content classifiers for text [8], [59], [11], [29], [15], [37], [47] or hash matching solutions for imagery [12], [4]. Beyond algorithmic solutions, platforms also rely on user reporting [6], and verdict appeals [40], [54]. For a more comprehensive overview, see Singhal et al. [50].

Datasets of harmful content. Public datasets of harmful content are currently scarce and often rely on crowd-sourced ratings, rather than ratings from trained experts. The datasets that exist primarily focus on a spectrum of hate speech and harassment [24], [38], [59], [27], and to a lesser extent, misinformation [42]. Previous studies have shown these datasets contain biases [7] and that the labels produced by crowdsourced workers contain significant disagreement [17], [27]. As such, we opted to use a non-public corpus of harmful content that reflects the reality of content moderation on a major platform backed by raters trained on real policies.

LLMs as classifiers. Since the emergence of powerful LLMs, a variety of researchers have investigated the zeroshot and k-shot capabilities of available models. For example, Chiu et al. used GPT-3 to detect racist and sexist language using k-shot prompts [5]. However, they cautioned that smaller LLMs might lack the sensitivity to differentiate between terms associated with targeted or protected groups and their context. Huang et al. conducted a similar experiment, targeting implicit hate speech with GPT-3 [22]. Rather than prompting, He et al. explored fine-tuning models for toxicity detection, achieving a 10% performance gain over existing baselines [21]. Bai et al. proposed a model alignment approach to enhance LLM sensitivity to harmful content by providing specifications and principles [3]. This enabled the model to critique its output and improve its awareness of offensive content. Similarly, Vishwamitra et al. explored identifying derogatory terms and generalizing detection via chain of thought using a BERT model [55]. Closest to our work, Weng et al. recently explored whether GPT-4 could achieve similar accuracy to human raters for a variety of moderation tasks [57]. Via a blog post, they reported that LLM performance approached that of reviewers with limited training, but fell short of expert reviewers. However, their post shared no experimental details (e.g., setup, prompt strategies, or design strategies). In short, while others have considered the use of LLMs for content moderation, we depart from the conventional design choice of LLMs as automatic content classifiers and focus instead on enhancing and maximizing the expertise of human raters.

## 3. Collaborative design patterns

We begin by outlining how LLMs can assist human experts with detecting harmful content in a variety of policy contexts (e.g., hate speech, misinformation). In practice, human ratings are critical to generating training and testing data for supervised abuse classifiers, triaging user reports of policy violations, and handling appeals of suspected nonviolations as shown in Figure 1. Due to the asymmetry in the scale between the volume of user-generated content requiring rating decisions and available human expertise for billion-user platforms, human raters are a scarce resource. Our vision is that LLMs can automate clear decisions around harmful content that do not require subtle human expertise and assist human raters in their deliberation process on the remaining content. Here, we enumerate five such collaborative design patterns along with their terminology and associated performance metrics.

Figure 1: Platforms rely on human raters to label data for supervised abuse classifiers, to triage user reports of suspected policy violations, and to determine the validity of user appeals that claim content is non-violative. We envision an LLM agent that optimizes which content gets sent to human raters and assists human raters in arriving at decisions.

<!-- image -->

## 3.1. Terminology

Content. Content or object refers to any user-generated data, such as comments, reviews, posts, and more. For the purposes of this work, we focus on text-based content, though emergent multi-modal LLMs would also allow for the classification of images, videos, audio, and other content.

Policy. A policy is any set of natural language rules that a platform uses to determine whether or not content should be prohibited for safety reasons. Examples include policies against scams, hate speech, and misinformation.

Verdict. We refer to the outcome of a policy determination as a verdict . A verdict may deem the content violative , thus triggering an escalation such as the removal of the content from the platform, or non-violative resulting in no further action. The choice of escalation is context dependent and outside the scope of this work.

Human rater. We assume the existence of a human rater : a human expert responsible for making policy decisions. In practice, their expertise-and thus accuracy-may vary due to ambiguity, necessary local context, a spectrum of familiarity with the policy, rapidly changing policies, or complex cases with competing policy interest (e.g., free speech concerns vs. potential for harm).

LLM rater. We refer to any LLM agent that assists with policy determinations as an LLM rater . As we discuss shortly, the assistance this LLM rater provides can vary in purpose: it can automate decision making, identify errors produced by human raters, or augment the decision making process of human raters.

Rater queue. We assume the existence of a rater queue that includes content-or objects-that should be evaluated against one or more policies.

## 3.2. Performance metrics

We assess the performance of LLM raters according to improvements in scaling, latency, and accuracy. While there are other potential benefits of LLM raters-such as improving the well-being of human raters analyzing harmful content [52]-these are highly context dependent and thus outside the scope of our study (beyond simply reducing the overall number of reviews performed, as discussed below).

M1 - Scaling. Human rating is a finite and expensive resource. Assuming that the cost of querying an LLM is less than that of querying a human rater, one can scale the volume of reviews beyond what was previously feasible by using LLMs to prioritize what content requires the expertise of human raters, meanwhile automating the bulk of rote decisions. Any scaling in practice is context dependent. As a rough feasibility estimate, Google Cloud charges $0.0005 per thousand characters of text input and output to PaLM 2; 1 Microsoft Azure charges $0.001 per thousand input tokens and $0.002 per thousand output tokens for GPT-3.5. 2 While there is limited public information on human rater salaries, data annotation services such as SageMaker charge $0.08 per object 3 -on the order of 100x compared to LLMs.

M2 - Reducing decision latency. Human rating incurs a decision delay t m on the order of seconds to minutes (not including time spent in a queue). Given the latency of querying an LLM as t m ′ for the same object, we can estimate the reduction in decision latency as t m -t m ′ .

M3 - Reducing false negatives. Human rating, despite relying on experts, is still subject to errors. If an LLM rater can outperform a human rater at identifying violations, this can lead to an overall reduction in false negatives (e.g., incorrectly missed violations) and potentially more consistent enforcement.

M4 - Reducing false positives. As above, if an LLM rater can outperform a human rater at identifying non-violations, this can lead to an overall reduction in false positives (e.g., incorrectly escalated violations) and potentially more consistent enforcement.

## 3.3. Modes of operation

We envision multiple modes of operating an LLM rater to improve content moderation as shown in Figure 2. Real world deployments will likely rely on a combination of some or all of these versions of LLM raters. We discuss the relative merits of each mode below.

¶ Pre-filtering [M1, M2]. For rater queues that are heavily skewed towards non-violative content (e.g., noisy user reports or rare incidents), an LLM rater can operate as a pre-filter before sending content to a human rater. Here,

1. https://cloud.google.com/vertex-ai/pricing \ #generative \ ai \ models

2. https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openaiservice/

3. https://aws.amazon.com/sagemaker/data-labeling/pricing/

Figure 2: Design patterns for using an LLM to assist human raters. We separate these into designs that attempt to optimize which content is sent to human raters ( ¶ , · , , ) and designs that attempt to improve the accuracy of human raters ( ' , ' ).

<!-- image -->

the LLM rater needs to achieve a minimum threshold T r of recall 4 to ensure that a majority of violative content is forwarded to a human rater, while also achieving a high degree of specificity 5 to ultimately dequeue non-violative content. Pre-filtering serves to free up raters to review more likely violative content while increasing the total volume of content reviewed ( M1 ). It may also potentially expedite decision making if the rater queue is non-saturated after filtering ( M2 ).

precision is sufficiently high. This escalation architecture serves to expedite decision making ( M2 ) and potentially avoid false negatives that a human rater may make ( M3 ) if the LLM rater can outperform a human rater in terms of precision and sensitivity. For sufficiently large volumes of violations, it may also allow additional scaling ( M1 ).

- Rapid escalation [M1, M2, M3]. For rater queues that may contain high-severity or emerging threats that requires immediate escalation, an LLM rater can operate as a fastpath escalation, entirely bypassing any human rater (or putting objects at the head of a queue). Doing so requires that the LLM rater achieves a minimum threshold T p of precision 6 and a high degree of recall to capture as much high-severity content as possible. Such a system might be deployed temporarily in response to an incident despite low precision (with a higher risk of appeals), or long-term if the
4. We use the standard machine learning definition of recall-or sensitivity-which is correctly identified violative samples divided by the total number of violative samples: TP/P .
5. We use the standard machine learning definition of specificity, which is the total number of correctly identified non-violative samples divided by the total number of non-violative samples: TN/N .
6. We use the standard machine learning definition of precision, which is correctly identified violative content divided by all content flagged as violative: TP/ ( TP + FP ) .
- , Autonomous rating [M1, M2, M3, M4]. For some policies, it may be possible for an LLM rater to achieve equivalent-or better-performance to human raters, thus enabling the full automation of a rater queue. This represents a more difficult challenge as the LLM must achieve both a minimum threshold for precision T p and recall T r , with both thresholds ideally exceeding the performance of human raters. As a safeguard, any appeals of LLM rater verdicts by users should not be sent to the same LLM rater. This operation mode has the potential to improve all performance dimensions of the rater queue.
- ' Human rater validation [M3, M4]. Rather than automating (some) decisions in a rater queue, an LLM rater can serve as a quality control system. Mechanistically, an LLM rater and human rater both rate the same content. If they disagree on the verdict-and the LLM rater has sufficient confidence-the same content can be sent to one or more additional human raters. The final verdict then consists of a majority vote across human raters. This quality check can bias towards identifying errant non-violative verdicts ( M3 ) or alternatively errant violative verdicts ( M4 ). Configuration

TABLE 1: Stratified sample of English comments identified by human raters at Google for violating one of four distinct policies, as well as a sample of non-violative comments. Examples have been paraphrased for privacy and redacted to minimize repeating harmful language.

| Policy type             | Example comments                                                                                                                                            | Sample size   |
|-------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|
| Hate Speech             | 'Because every single [redacted] steals and commits crimes. It's their culture.' 'Sadly due to mass immigration of low IQ savages [redacted] is a cesspit.' | 10,000        |
| Violent Extremism       | 'Lethal attachments are a dime a dozen. Ill be a mass shooter in no time.' 'I hope more people like [Christchurch shooter] emerge and prove them right.'    | 10,000        |
| Harassment              | 'Go find the tallest building then jump bro its literally not that serious.' 'Somebody SHUT that nasal, whiny little [redacted] up!'                        | 10,000        |
| Election Misinformation | 'Covid was a cover to remove [redacted] through fraudulent mail in voting.' 'YOU ARE AWARE ARN,T YOU THE VOTING MACHINES WERE RIGGED.'                      | 10,000        |
| Non-violative           | 'Bro you better apologize, you messed with wrong people.' 'Average IQ in this comment section is 90.'                                                       | 10,000        |

of the quality check requires balancing the total number of additional human ratings an LLM rater can trigger versus the lift in accuracy.

- ' Human rater assistance [M2, M3, M4]. An LLM rater can also help human raters understand the context of potential violative content. During rating, a human rater might engage with an LLM rater to receive an explanation of why content is violative or not-such as highlighting specific passages of content that may violate a policy. This augmentation can help expedite rating ( M2 ) while also drawing attention to critical context that might otherwise be missed, improving overall accuracy ( M3 , M4 ). However, there is also the risk of biasing human raters to agree with the LLM rater.

determined were non-violative of all Google's policies. 7 All comments are in English, which is one of the most popular languages on Google. For each sample, we have the text of the comment and a binary label (e.g., 1 if violative, 0 if non-violative). Each policy strata reflects a randomized sample drawn over a three month period from August 2023October 2023, with the exception of election misinformation which was drawn from October 2022-October 2023. For all our experiments, we use a balanced dataset of violative samples and non-violative samples per policy to evaluate the capabilities and tradeoffs of LLM rating. Later in Section 7, we discuss the real-world pilot of our proposed techniques on live rating queues on the natural distribution of violations and non-violations.

## 4. Dataset

In order to explore the feasibility of LLM raters and our collaborative design patterns, we obtain a real-world dataset of 50,000 human-rated violative and non-violative user comments for a variety of types of harmful content. We discuss this dataset, our approach to validation, and limitations that stem from our approach.

## 4.1. Policy violations and non-violations

Our dataset consists of a stratified sample of 40,000 unique, user-generated comments that human policy raters at Google identified as violative for one of four distinct policies: hate speech, violent extremism, harassment, and election misinformation. This dataset is ecologically valid, representing the reality of human ratings at-scale for diverse user bases. We focus on these policies as it allows us to assess the generalizability of an LLM rater to multiple safety concepts, while balancing the overhead of querying LLMs with tens of thousands of comments per experimental design. We provide a sample of violative comments for each policy in Table 1. Additionally, we have a sample of 10,000 unique, user-generated comments that human raters

## 4.2. Validation

For the purposes of our study, we treat the labels from human policy raters as ground truth . In practice, these labels may include some errors. As an assessment of data quality, we randomly sampled 500 comments, stratifying this selection to include 100 comments per each policy type in our study-including non-violations. Two researchers independently labeled each comment as violative or nonviolative according to the public policy text, with a third researcher helping to resolve all disagreement. We also allowed for a third label of 'missing context', in the event the three researchers could not render a judgement without the comment's surrounding context (e.g., 'They look like aliens' is ambiguous for who 'they' refers to). 8

We present the rate of agreement and disagreement between the original expert labels and validation labels in

7. In practice, Google's policies are more expansive than the four we evaluate. As such, non-violative content excludes scams and many other forms of harmful content. As we show, many of these non-violative comments border policies in some way, leading to the potential for false positives.

8. Unlike our research team, policy raters had access to the surrounding context (e.g., the page the comment appeared on, other comments in a conversation) when making their decision.

TABLE 2: Results of our independent validation of 500 ground truth labels. We find 0-2% of comments flagged by human policy raters as violations may be non-violations. Another 8% of comments deemed non-violations may be violations.

| Policy                  | Agree   | Missing context   | Disagree   |
|-------------------------|---------|-------------------|------------|
| Hate Speech             | 90%     | 8%                | 2%         |
| Violent Extremism       | 96%     | 4%                | 0%         |
| Harassment              | 91%     | 7%                | 2%         |
| Election Misinformation | 98%     | 0%                | 2%         |
| Non-violative           | 77%     | 15%               | 8%         |

Table 2. For policy violations, we find just 0-2% of comments may be non-violations. Another 0-8% of comments lacked sufficient context for us to make an absolute determination. For example, 'this mental illness stuff is getting out of hand fr' was flagged by an expert as hate speech (likely due to being transphobic and claiming transgender individuals have a mental illness), but our validation lacks the surrounding context, so we cautiously assigned a label of missing context. The remaining 90-98% of comments were clearly violative. For non-violative content, we find 8% of comments may violate one of the four policies in our study. Another 15% might be construed as violative depending on the missing context. For example, 'Shoot that dirtbag horse!' might be threatening violence, or be about a video game, so we assigned a label of missing context. The remaining 77% of comments were clearly non-violative.

We caution that the researchers involved in validation are not trained policy raters. It is clear from our validation that many non-violative comments are offensive or incendiary, but not necessarily to the level of a policy violation. Through this lens, we argue it is methodologically sound to treat the original expert labels as ground truth. The consequence on our measurements is that an LLM may have an upper bound of 98-100% for recall, and an upper bound of 92% for precision, if validation labels (e.g., 'Disagree' in Table 2) are in practice more accurate than the original expert labels.

## 4.3. Ethics and Limitations

Our methodology incurs a number of limitations. Our dataset is limited to four types of harmful content. While these types cover some of the most pressing emerging threats, enforcement may differ from platform to platform, even if policy language may be similar. Likewise, the distribution of comments from Google may not generalize to other platforms. These subtleties may result in variable performance when evaluated on other datasets. Finally, in the event of invalid ground truth labels, we may inaccurately estimate the performance that LLMs can achieve. We note the researchers in this study never had access to any identifying information associated with comments (e.g., usernames or account activities), and that all comments were posted publicly.

## 〈 Misinformation and Disinformation Policy 〉

- 1) Comments should not mislead census participants about the time, place, means, or eligibility requirements of the census.
- 2) Comments should not make false claims that could materially discourage census participation.
- 3) Comments should not mislead voters about the time, place, means, or eligibility requirements of voting.
- 4) Comments should not make false claims that could materially discourage voting.
- 5) Comments should not make false claims related to the technical eligibility requirements for current political candidates and sitting elected government officials to serve in office.
- 6) Comments should not encourage others to interfere with democratic processes.
- 7) Comments should not contain hacked info, the disclosure of which may interfere with democratic processes.
- 8) Comments should not make false claims that widespread fraud, errors, or glitches occurred in certain past elections to determine heads of government.

〈 /Misinformation and Disinformation Policy 〉

Question: You are an expert content moderator. Does the following comment violate the Misinformation and Disinformation Policy?

Comment: '[COMMENT]' Answer:

Figure 3: Initial prompt derived from Google's public policy around census and election misinformation. Across all our experiments, this policy language remains static.

## 5. Building LLM raters

We conduct an ablation study to determine how different choices of prompts and models affect the performance of an LLM rater in terms of its precision, recall, specificity, and accuracy. As previously outlined in Section 3, the different operating modes of an LLM rater require achieving good performance in only a subset of the metrics we evaluate in order to be suitable for practical deployment.

## 5.1. Ablation parameters

Baseline policy specification. Based on early experimentation, we opted to seed all our prompt variants with a policy description derived from the harmful content policies shared publicly by Google [14]. We reformatted all of these policies into an enumerated list that is easily interpretable by an LLM. We share an example in Figure 3 and provide the specification for all four policies we consider in the Appendix.

Zero-shot vs. few-shot. One variable we consider is whether an LLM requires examples of comments and verdicts to render a decision. In our zero-shot variant, we provide no examples but prepend a 'dummy' policy and questionanswer pair to prime the LLM on our expected output format (see Appendix). For our few-shot variants, we provide a list of sample comments along with their human rated verdict, an example of which we show in Figure 4. We opt for

Question: You are an expert content moderator. Does the following comment violate the Misinformation and Disinformation Policy?

Comment: 'President Joe Biden hit them with Covid-19 to help him steal an election'

Answer:

Yes

Keywords: covid-19 - steal - election

--

Comment:

'[COMMENT]'

Answer:

Figure 4: A few-shot prompt variant that includes both an example policy-relevant comment and answer, and keyword context. The comment under evaluation appears after all examples.

five examples: three comments that violate the policy under consideration and two that do not violate any policy.

We explored three options for selecting these examples: (1) first, we used static, hand-picked examples. We chose these examples to be representative of the overall problem space and the policy under question; e.g., for hate speech we chose violative examples that targeted different protected groups. After observing the success of this strategy (as discussed below in Section 5.2), we next experimented with (2) dynamically identifying semantically 'close' comments in terms of their embedding distance; and (3) purposefully injecting errors into the dynamically chosen samples to understand the sensitivity of prompts to noise.

Keyword context and chain-of-thought. Another variable we consider is whether providing context on the most salient terms from violative comments assists an LLM with rendering an accurate verdict-a form of chain-of-thought [56]. As part of our hand-picked few-shot examples, we include (manually chosen) keyword context as shown in Figure 4.

Model selection. Finally, we consider how different models affect performance. We query all of our prompt variants using both the PaLM 2 text-bison and text-unicorn models (with the latter being larger than the former), available via Google's Vertex AI API [13], each with a context window of 8192 tokens. For all experiments we use a fixed temperature of zero, which means the LLM always picks the most probable next token, and generate one token for the LLM response. This determinism ensures that an LLM produces the same output across subsequent executions, which is critical for operating a classifier in practice and for evaluating errors that might otherwise be transient. We parse the LLM output, treating 'Yes' (i.e., 1) as a violative verdict and 'No' (i.e., 0) as non-violative verdict. While we use only this binary output in this section, we discuss in Section 7 the potential benefits of having the LLM output more information, such as a list of keywords and the policy entry that most contributed to its decision. We note that PaLM 2 models knowledge cutoff is mid-2021, thus there is no risk of our data from October 2022-October 2023 appearing in the model's training data [16].

For privacy reasons, we were unable to evaluate using GPT-4 or Claude-2. Likewise, Gemini Pro and Ultra had not been released at the time of our experimentation. We emphasize that our goal is to assess the general feasibility of content moderation via LLMs, rather than benchmarking the relative merit of different LLM providers. Additionally, individual LLM idiosyncrasies stemming from instruction tuning and reinforcement learning would likely require adjusting prompts per LLM architecture. Furthermore, it is cost prohibitive to query many models with all the prompt variants we evaluate in this study; as it is, with only two models we already perform half a million queries.

## 5.2. Single policy enforcement

We begin by examining the accuracy of LLM raters that are specialized to enforce only a single policy at a time, evaluating each LLM rater on 10,000 comments that violate the associated policy, and 10,000 comments that violate no policy. We present the results of our zero-shot prompt, few-shot prompt with hand-picked examples, and the handpicked few-shot prompt with keyword context in Table 3, for both the models we used. (We evaluate the other two few-shot variants in subsequent experiments.)

Compared to human raters, the best prompt and model combination achieves 98.7% accuracy for election misinformation, 90.3% accuracy for hate speech, 89.3% accuracy for violent extremism, and 87.2% accuracy for harassment.

Comparing models. To compare the performance of models, we calculate a McNemar's test statistic comparing the best performing prompt for both text-unicorn and text-bison as evaluated on the same test set. Overall, text-unicorn outperformed text-bison , with a relative lift of 0.2%-2.4% between the best prompts ( p &lt; 0 . 001 , except for hate speech where p = 0 . 177 ). This modest performance gap indicates that platforms can opt for smaller and less costly models for some policies (especially keeping in mind that text-bison is an order of magnitude less expensive than text-unicorn , costing $0.00025 per thousand input characters as compared to $0.0025), but that the scaling laws of LLMs [25] still favor larger models for accurate policy interpretation.

Comparing prompt variants per model. To compare the performance of prompt variants, we calculate a McNemar's test statistic with the zero-shot prompt as the baseline. We find that our few-shot prompt yielded statistically equivalent or better performance overall for both text-bison and textunicorn , with the exception of harassment where handpicked examples sent to text-unicorn degraded accuracy by 1% ( p &lt; 0 . 001 ). On the other hand, examples carry an additional cost in terms of increasing the length of the prompt (in the case of violent extremism, which has the shortest policy specification, by as much as 61%) and thus the cost to evaluate the comment.

Keyword context appears unnecessary for text-unicorn , but does yield a 6.2% gain for violent extremism, and a 1.1% gain for harassment for text-bison ( p &lt; 0 . 001) . At the same time, keyword context lifted the recall of all policies

TABLE 3: Performance of text-bison and text-unicorn at detecting harmful content in English. We report on three prompt variants: our zero-shot variant (acting as the baseline and containing just the policy language), our few-shot variant with hand-picked examples, and our hand-picked few-shot variant with keyword context. P-values indicate whether the differences between a variant and the baseline are statistically significant.

| Policy                  | Model   | Examples   | Keywords   | Precision   | Recall      | Specificity   | Accuracy    | ∆         | p-value         |
|-------------------------|---------|------------|------------|-------------|-------------|---------------|-------------|-----------|-----------------|
| Hate                    |         | ×          | ×          | 86.0%       | 95.1%       | 84.5%         | 89.8%       | -         | -               |
| Hate                    | bison   |            | ×          | 86.6%       | 94.8%       | 85.3%         | 90.1%       | 0.3%      | 0.003           |
| Hate                    |         | ×          |            | 86.4%       | 94.7%       | 85.0%         | 89.9%       | 0.1%      | 0.336           |
| Hate                    | unicorn |            | ×          | 85.5%       | 96.6%       | 83.6%         | 90.1%       | -         | -               |
| Hate                    |         |            | ×          | 86.4%       | 95.5%       | 85.0%         | 90.3%       | 0.2%      | 0.090           |
| Hate                    |         |            |            | 86.5%       | 95.6%       | 85.0%         | 90.3%       | 0.2%      | 0.026           |
| Violent Extremism       |         | ×          | ×          | 90.9%       | 68.2%       | 93.2%         | 80.7%       | -         | -               |
|                         | bison   |            | ×          | 88.6%       | 81.8%       | 89.5%         | 85.6%       | 5.0%      | < 0.001         |
|                         |         |            |            | 87.9%       | 85.5%       | 88.2%         | 86.9%       | 6.2%      | < 0.001         |
|                         | unicorn | ×          | ×          | 89.4%       | 86.6%       | 89.7%         | 88.1%       | -         | -               |
|                         |         |            | ×          | 89.6% 87.8% | 88.9% 91.3% | 89.7% 87.3%   | 89.3% 89.3% | 1.2% 1.2% | < 0.001 < 0.001 |
|                         |         | ×          |            | 82.3%       | 85.9%       | 81.5%         | 83.7%       | -         | -               |
| Harassment              | bison   |            | × ×        | 81.9%       | 87.2%       | 80.7%         | 84.0%       | 0.3%      | 0.123           |
| Harassment              |         |            |            | 81.9%       | 89.2%       | 80.3%         | 84.8%       | 1.1%      | < 0.001         |
| Harassment              |         | ×          | ×          | 82.9%       | 93.7%       | 80.7%         | 87.2%       | -         | -               |
| Harassment              | unicorn |            | ×          | 81.0%       | 94.6%       | 77.8%         | 86.2%       | -1.0%     | < 0.001         |
| Harassment              |         |            |            | 80.1%       | 95.9%       | 76.2%         | 86.1%       | -1.1%     | < 0.001         |
| Election Misinformation | bison   | ×          | ×          | 96.1%       | 96.1%       | 96.1%         | 96.1%       | -         | -               |
| Election Misinformation |         |            | ×          | 95.7%       | 99.4%       | 95.5%         | 97.5%       | 1.3%      | < 0.001         |
| Election Misinformation |         |            | ×          |             | 98.4%       | 98.2%         |             | -         |                 |
| Election Misinformation | unicorn | ×          |            | 98.2%       |             |               | 98.3%       |           | -               |
| Election Misinformation |         |            | ×          | 98.4%       | 99.0%       | 98.4%         | 98.7%       | 0.4%      | < 0.001         |
| Election Misinformation |         |            |            | 97.8%       | 99.0%       | 97.8%         | 98.4%       | 0.1%      | 0.370           |

with text-unicorn -at the cost of precision. This suggests that keyword context can be omitted for LLM raters designed to automate decision where accuracy is more important than recall. Keywords may still play a role for smaller models.

Accuracy vs. content length. A final dimension we explore is the effect of longer, possibly extraneous text on classification accuracy. Of the comments in our dataset, 50% have 11 or fewer words (and 59 characters) and 90% have 51 or fewer words (and 282 characters). We present a breakdown of accuracy for an LLM rater configured to use text-unicorn with our few-shot prompt across policies, stratified by character length in Figure 5. We find that our LLM rater declines in accuracy for longer comments. This may be a consequence of LLMs not giving enough attention to short violative passages in comments that are otherwise innocuous [32]. A potential solution would be to segment long-form text and query individual passages, but this is likely prohibitively expensive if the prompt instructions remain longer than the text under evaluation.

## 5.3. Dynamic few-shot variants

Given that our few-shot prompt variant with hand-picked examples reliably outperforms the zero-shot variant, we next examine how the quality of examples-in terms of both relevance and label accuracy-affects classification accuracy. Similarly to retrieval augmented generation (RAG) [30], we dynamically generate a prompt for a given comment that includes five semantic nearest neighbors.

For semantic similarity, we use textembedding-gecko to produce 768-dimensional vector embeddings and an Annoy index [51] with 200 trees for fast, top-N approximate nearest-neighbor selection, with one index for 10,000 violative samples and one index for 10,000 non-violative samples per policy under evaluation. When querying these indices for the neighbors of a comment, we exclude the comment under evaluation as a valid neighbor. We then pick the three closest violations in our Annoy index, and the two closest non-violations.

We present our results in Table 4, comparing to the performance of our hand-picked few-shot variant with a McNemar's test statistic. For text-unicorn , we observe a performance change between -0.5% and 3.9% ( p &lt; 0 . 001 ). Dynamic examples yielded the best overall performance across

TABLE 4: Performance of our few-shot variant with examples chosen dynamically based on semantic distance from previously rated content. As a baseline, we use the hand-picked few-shot variant. This prompt variant yielded our best performance across all variants, apart from election misinformation.

| Policy                  | Model         | Precision   | Recall      | Specificity   | Accuracy    | ∆         | p-value         |
|-------------------------|---------------|-------------|-------------|---------------|-------------|-----------|-----------------|
| Hate Speech             | bison unicorn | 83.3%       | 97.8%       | 80.4%         | 89.1%       | -0.9%     | < 0.001 < 0.001 |
|                         |               | 88.2%       | 94.8%       | 87.3%         | 91.1%       | 0.8%      |                 |
| Violent Extremism       | bison unicorn | 84.4% 92.2% | 95.2% 89.7% | 82.3% 92.5%   | 88.8% 91.1% | 3.1% 1.8% | < 0.001 < 0.001 |
| Harassment              | bison         | 79.0%       | 98.0%       | 74.0%         | 86.0%       | 2.1%      | < 0.001         |
|                         | unicorn       | 85.7%       | 96.4%       | 83.9%         | 90.1%       | 3.9%      | < 0.001         |
| Election Misinformation | bison         | 87.1%       | 99.7%       | 85.3%         | 92.5%       | -5.0%     | < 0.001         |
| Election Misinformation | unicorn       | 99.0%       | 97.4%       | 99.1%         | 98.2%       | -0.5%     | < 0.001         |

Figure 5: Accuracy of text-unicorn for our hand-picked fewshot prompt variant. We segment our evaluation corpus into buckets of 0-9 characters, 10-19 characters, and so on up to 100+ characters. For each sample, we display error margins for a confidence level of 95%. (Note the truncated Y-axis.)

<!-- image -->

| Policy                  | Model         | Accuracy    | ∆           | p-value         |
|-------------------------|---------------|-------------|-------------|-----------------|
| Hate Speech             | bison unicorn | 88.4% 88.9% | -1.7% -1.3% | < 0.001 < 0.001 |
| Violent Extremism       | bison unicorn | 86.6% 86.6% | 0.9% -2.7%  | < 0.001 0.023   |
| Harassment              | bison unicorn | 84.7% 86.8% | 0.7% 0.6%   | < 0.001 < 0.001 |
| Election Misinformation | bison unicorn | 94.0%       |             | < 0.001 < 0.001 |
|                         |               | 90.3%       | -7.2% -4.6% |                 |

all prompt variants, other than for election misinformation. For text-bison , dynamic examples hampered performance for election information (-5.0%) and hate speech (-0.9%), but improved accuracy for violent extremism (3.1%) and harassment (2.1%).

That said, we find the performance of dynamic few-shot examples is sensitive to inaccurate labels. As an experiment, we selected the same semantically close comments but randomly flipped the verdict of one example to simulate a labeling error. We present the impact of these errors in Table 5, again comparing to our hand-picked few-shot variant with a McNemar's test statistic. For text-unicorn , hate speech detection degraded by 1.3%, while election misinformation detection degraded by 4.6% (all p &lt; 0 . 001 ). We find text-bison was more sensitive to noise, with performance degrading by as much as 7.2% ( p &lt; 0 . 001 ). Harassment stands out for both model sizes, where noisy labels yielded better results than our hand-picked examples but worse accuracy than our zero-shot variant for text-unicorn , or accurate dynamic labels.

TABLE 5: Performance for our few-shot variant with dynamic examples, but where we intentionally introduce a random verdict error for one example. As a baseline, we use the hand-picked few-shot variant. Both models are sensitive to errors, though losses in accuracy were lower for textunicorn .

Both of our experiments suggest that dynamically selecting few-shot examples can boost performance and potentially account for emerging concepts (e.g., glorifying the name of a violent extremist, or a new hate term) not present in the training corpus of an LLM or the policy body of a prompt. However, queue operators need to ensure that examples favor high-quality labeled data to minimize any performance loss.

## 5.4. Multi-policy enforcement

While our focus thus far has been on how to optimize LLM raters for individual policies, in practice, platforms have tens of policy categories that need to be assessed against any object. As an alternative to sending content to N specialized LLM raters, we explore the feasibility of deploying one zero-shot prompt encompassing multiple policies. To do this, we compile all our policy text (totalling 40 clauses) into a single prompt. We then compare this accuracy against our zero-shot, per-policy prompts on the same test corpus and calculate a McNemar's test statistic. We present our results in Table 6. We find our multi-policy prompt performs worse for both text-bison (-2.6-10.9%) and text-unicorn (-2.2-13.7%). The most impacted policy was

TABLE 6: Performance for a single prompt covering all four content safety policies, with its 40 clauses ordered as hate speech, harassment, violent extremism, and election misinformation. Policies towards the end of the context window see a drop in accuracy compared to a prompt only related to that policy.

| Policy            | Model         | Accuracy    | ∆           | p-value         |
|-------------------|---------------|-------------|-------------|-----------------|
| Hate Speech       | bison unicorn | 86.3% 87.5% | -3.4% -2.6% | < 0.001 0.002   |
| Violent extremism | bison unicorn | 77.3% 79.0% | -3.4% -9.2% | < 0.001 0.023   |
| Harassment        | bison unicorn | 81.1%       | -2.6%       | < 0.001 0.055   |
| Election          | bison unicorn | 85.2%       |             | < 0.001 < 0.001 |
|                   |               | 85.0%       | -2.2%       |                 |
|                   |               |             | -10.9%      |                 |
|                   |               | 84.6%       |             |                 |
|                   |               |             | -13.7%      |                 |
| Misinformation    |               |             |             |                 |

election misinformation, likely due to it appearing at the end of the prompt's context window.

As such, prompts need to control for the verbosity of policy language. Overly long policies will likely see a degradation in classification accuracy. That said, there are cost tradeoffs. For a transformer-based model, the processing cost is O ( n 2 ∗ m ) where n is the input length and m is the output length (which is fixed at 1 for binary answers), which favors short, specialized prompts. However, other factors such as the base cost of running an inference and the size of the prompt may favor multi-policy prompts. As a concrete estimate using the Google Cloud costs presented in Section 3.2, the average character length of the comments in our dataset, and the four policies we consider, the cost of using text-unicorn to evaluate a queue of 50,000 comments is roughly $762 using a multi-policy prompt and roughly $1,137 using single-policy few-shot prompts (in which each comment is fed to one LLM rater per policy). We stress that these are estimates and that there are other ways to optimize prompts for cost.

## 5.5. Summary

Across all metrics, the overall best choice of model was text-unicorn (the larger model). In terms of our prompt variants, we generally saw the best performance from the few-shot variant with dynamically selected examples (with the caveats mentioned previously about cost and needing to ensure the accuracy of these examples). As such, for the rest of the paper we consider only the results of querying text-unicorn with this prompt variant. We acknowledge, however, that models and prompt engineering practices are evolving rapidly, and given our focus on the general feasibility of using LLMs for content moderation we did not experiment with more advanced approaches like automated prompt optimization (APO) [61], [62], [45]. We thus leave an exploration of the effectiveness of this, other practices, and even larger models as interesting future work.

Figure 6: Precision vs. recall for our adaptive few-shot example policy prompt and text-unicorn . Using the probability of tokens predicted by an LLM, we can flexibly alter whether a prompt favors precision or recall.

<!-- image -->

## 6. Utilizing LLM raters

Based on the findings of our ablation study, Section 5, we explore the suitability of our most accurate prompt varianttext-unicorn with dynamic few-shot examples-in satisfying each of the collaborative design patterns outlined earlier in Section 3. As part of this, we introduce a technique that allows a single prompt to flexibly adapt to every design pattern.

## 6.1. Dynamically tuning LLM raters

Our experiments show that one prompt variant might yield the best precision, while another yields the best recall or specificity. In practice, maintaining multiple variants per policy-especially at the speed that policies might adaptis prohibitively expensive. Instead, we examine how to use the probabilities generated by LLMs (e.g., top-k scores for returned tokens) to create a configurable decision boundary to support multiple use cases without needing to change the underlying prompt. Using text-unicorn with a dynamic few-shot example prompt, we configure the model to return p=Score('Yes') ; i.e., the probability that the next generated token after our prompt is 'Yes'. 9 From this probability, we define a sliding decision threshold T , where we treat all p ≥ T as a policy violation and all other samples as nonviolative. We then calculate the precision and recall at each threshold T .

We present the precision and recall curve of this approach in Figure 6. Misinformation stands out as its overall accuracy is 98.2%, while the other policies have an accuracy of 90.1-91.1%. The token probabilities returned by an LLM can effectively be interpreted as a confidence score. Comments that receive a 'Yes' verdict can still be treated as

9. In experimentation, p=Score('No') was equally viable, though we note the two are not guaranteed to add to 1.0.

TABLE 7: Performance of an LLM rater pre-filtering nonviolative comments with minimum recall threshold of 95% and 99%. The higher variance in the pre-filtering rate for 99% recall may be due to label inaccuracy, where the LLM is highly confident a ground truth violation is non-violative, requiring a very low threshold T that passes too much content on to a human rater.

| Policy                  | Recall threshold   | Pre-filtering rate   |
|-------------------------|--------------------|----------------------|
| Hate Speech             | 95.5%              | 86.6%                |
| Violent Extremism       | 95.0%              | 85.8%                |
| Harassment              | 95.5%              | 85.2%                |
| Election Misinformation | 95.1%              | 99.3%                |
| Hate Speech             | 99.1%              | 75.1%                |
| Violent Extremism       | 99.1%              | 54.5%                |
| Harassment              | 99.1%              | 71.1%                |
| Election Misinformation | 99.0%              | 98.2%                |

non-violative if the LLM does not meet the requisite confidence threshold T . For scenarios where recall is imperative, T &lt; 0 . 5 is most suitable; for precision, T &gt; 0 . 5 is most suitable.

## 6.2. Collaborative design pattern performance

We simulate the performance of each collaborative design pattern-previously discussed in Section 3-assuming a single rating queue per policy that contains a 1:1 mixture of violative and non-violative content.

Pre-filtering. A pre-filtering LLM rater aims to remove clearly non-violative content from a rating queue, while falling back on human rater expertise for borderline or egregious content. An LLM rater could remove 54.5-98.2% of comments from our simulated rater queue due to being non-violative, while ensuring 99% of violative content is sent to a human rater (Table 7). If constraints are relaxed and the LLM rater need only achieve a recall of 95%, then an LLM rater could remove 85.2-99.3% of non-violative comments from our simulated queues.

Rapid escalation. A rapid escalation LLM rater aims to escalate clearly violative content without requiring verification by a human rater, while falling back to human raters on all other content. An LLM rater could automatically escalate 48.8-99.7% of violative content with a precision of 95% (Table 8). A precision threshold greater than 99% is not feasible for hate speech and harassment, likely due to our ground truth incorrectly labeling some hate speech and harassment as non-violative. For the remaining policies, an LLM rater could automatically escalate 41.5-97.4% of violative content.

Autonomous rating. An autonomous LLM rater aims to handle ratings without any fallback to human raters. In practice, such an LLM rater achieves only 90.1-98.2% of the accuracy of human raters (Table 9). As such, the

TABLE 8: Performance of an LLM rater rapidly escalating violative content with minimum precision of 95% and 99%. An N/A means the targeted precision is currently not achievable on our dataset.

| Policy                  | Precision threshold   | Violations escalated   |
|-------------------------|-----------------------|------------------------|
| Hate Speech             | 95.2%                 | 60.6%                  |
| Violent Extremism       | 95.1%                 | 82.5%                  |
| Harassment              | 95.2%                 | 48.8%                  |
| Election Misinformation | 95.0%                 | 99.7%                  |
| Hate Speech             | 99.0%                 | N/A                    |
| Violent Extremism       | 99.0%                 | 41.5%                  |
| Harassment              | 99.0%                 | N/A                    |
| Election Misinformation | 99.0%                 | 97.4%                  |

TABLE 9: Performance of autonomous rating for our adaptive few-shot example policy prompt and text-unicorn .

| Policy                  | Accuracy   |
|-------------------------|------------|
| Hate Speech             | 91.1%      |
| Violent Extremism       | 91.1%      |
| Harassment              | 90.1%      |
| Election Misinformation | 98.2%      |

aforementioned collaborative design patterns may be more suitable given the current capabilities of LLMs.

Human rater validation. Our validation LLM rater aims to improve overall decision making accuracy by identifying likely human errors. For our simulated queues, we reflect on the 80,000 rating decisions an autonomous LLM rater would have made and compare them to our ground truth labels from human raters. Our LLM rater disagreed with human raters on 5,896 comments, or 7.4% of the time. We randomly sampled 400 points of disagreement, stratifying this selection to include 100 comments for each simulated policy rating queue. We then manually reviewed each comment using the same methodology as in Section 4.2 to determine whether researchers agreed with the policy expert or the LLM rater. We treat these as tie-breaking ratings . 10

We present our results in Table 10. For hate speech, our tie-breaking rating agreed with LLMs 49% of the time, versus the ground truth 43% of the time. As an illustrative example, our LLM rater flagged 'nice [thumbs up emoji] 88', a Nazi reference, which was potentially missed by the human rater. However, our LLM rater missed 'Cull these knickers', a likely slur. For election misinformation, tie-breaking ratings matched those of human raters more often than LLMs-52% versus 43% respectively. The loss in accuracy here is due to our LLM rater overindexing on any form of misinformation (particularly COVID-19, but also conspiracy theories) which fell outside the stated policy. In other cases, our LLM rater missed a shorthand of misinformation like '80 million dead people,' a census-

10. As with our earlier validation, we caution researchers are not trained policy experts, so concurrence with an LLM may be inaccurate.

| Policy                  | Human correct   | LLM correct   | Missing context   |
|-------------------------|-----------------|---------------|-------------------|
| Hate Speech             | 43%             | 49%           | 8%                |
| Violent Extremism       | 50%             | 34%           | 16%               |
| Harassment              | 47%             | 43%           | 10%               |
| Election Misinformation | 52%             | 43%           | 5%                |

TABLE 10: Breakdown of tie-breaking ratings for instances where an LLM rater disagreed with our ground truth. We indicate whether the tie-breaking vote agreed with the ground truth (human correct), with the LLM rater (LLM correct), or whether critical context was missing to render a tie-breaking rating.

related claim that more people voted in 2020 than was possible. For violent extremism, tie-breaking ratings most often concurred with human raters (or lacked context), in part due to the policy more cautiously flagging any mention of terrorist groups, whereas the LLM appeared to apply more of a contextual lens.

Taken as a whole, our qualitative analysis suggests that pairing LLM raters with human raters can measurably improve the accuracy of decision making. It also demonstrates that our LLM raters may be more accurate than our ground truth indicates. In practice, queue operators can configure the number of tie-breaking ratings using a higher precision score threshold.

Human rater assistance. An LLM rater assistant aims to provide critical context to human raters as they render verdicts. As our dataset and analysis is retroactive, we defer evaluation of this design pattern to our real-world experiments.

## 7. LLM raters in the real world

To demonstrate the feasibility of LLM raters, we piloted the integration an LLM rater into a live rating queue at Google containing English content. The LLM rater served two purposes: to optimize what content went to human raters and to assist human raters in arriving at a verdict.

Prompt design. The rating queue in our pilot triages usergenerated reports of potentially harmful content related to 20+ policies. Roughly 90% of these reports are inaccurate, with human raters ultimately determining content is nonviolative. Due to engineering and cost complexity, we limited our design to a single, multi-policy prompt covering all of these policies. We used text-unicorn for our model. Per our earlier analysis, we found text-unicorn 's accuracy degraded with long policies. We mitigated this by simplifying all of the policy clauses with an emphasis on recall. For example, a policy against dehumanizing a person based on their race, or stereotyping someone based on their race, might be up-leveled to a single statement against talking about a person's race whatsoever. Any false positives in a real deployment would be safeguarded by human raters. Conversely, quickly identifying errant user reports would better optimize human rater expertise.

Optimizing human rater expertise. We ran a pilot of our LLM rater in a shadow mode on a random sample of N=2,700 objects over a 30-day period, exclusively for English content. This non-enforcement ensured our LLM rater did not impact the quality of the rating queue, while allowing us to evaluate the efficacy of our proposed strategy. We sent every sampled object to both our LLM rater and the human rater process. 11 Over this 30-day period, we estimate that for a fixed recall of 95.1%, our LLM rater could reduce the volume of content requiring rating by 41.5% (e.g., prefiltering design pattern).

Improving accuracy of verdicts. As a separate pilot, we configured our LLM rater to output not just a verdict, but also keywords explaining the verdict (e.g., human rater assistance design pattern). As a within-subjects experiment to human raters who opted-in to the keyword feature, we surfaced these keywords for two weeks, by highlighting their appearance within the original text content rated by humans (N=500+ objects), comparing it against ratings made by the same human raters in the two week prior period conducted without support from the LLM (N=500+). Again, this was exclusively for English content. Recall for human ratersjudged via existing quality control systems-increased by 9% absolute ( p &lt; 0 . 001 ), while precision increased by 11% absolute ( p &lt; 0 . 001 ). There was no statistically significant change in the time it took to review content.

## 8. Discussion

In light of our findings, we discuss the benefits of LLM raters, potential risks, optimization strategies for improving performance, and research opportunities for the future.

## 8.1. Benefits

Scale &amp; maintenance. LLM raters can optimize available human expertise to a scale that was previously costand toil-prohibitive. While the current price per inference makes LLM raters best suited for rating only content that is sent to existing human rater queues, in the future, LLM costs are likely to decrease. This points to a possibility of LLM raters acting as scaled classifiers, particularly by fine-tuning smaller LLMs using individual policies and example comments. Such an architecture would minimize the training data required compared to existing classifiers, with LLM raters requiring only tens of samples for fixed fewshot prompts, hundreds of samples for adaptive few-shot prompts, or thousands of samples for fine-tuning.

Rapid response &amp; iteration. LLM raters enable policy experts to minimize the time between when a threat emerges and when a platform deploys a protection. Policy experts can distill their requirements into a simple set of instructions that an LLM rater can immediately enforce. This agility

11. In practice, a single piece of content might be rated by multiple human raters and de-conflicted according to Google's processes. We use the final verdict after any such processes.

in adapting policy language-where policy experts rather than engineers can directly iterate on prompts-is critical to responding to the global landscape of user concerns, threat actors, and regulations. We note this can be in tension with fine-tuning, which introduces both a computational and technical-expertise overhead compared to few-shot prompts that are more accessible to policy writers. Paired with other scaled defense-in-depth systems, LLM raters allow for upstream detectors to be less accurate (and thus easier to develop and deploy), with LLM and human raters correcting for any errors before any enforcement action.

Consistency. Evolving policies, different cultural norms, and different levels of expertise mean that two human raters can arrive at different verdicts. This is particularly true when human raters are in the midst of adapting their processes to policy changes. LLM raters allow for more consistent-and potentially unbiased-enforcement, acting as a safety net.

Reducing emotional burden. LLM raters offer an opportunity to automatically identify the most egregious harmful content, removing the need for any human to have to view it. While human raters would still be involved in borderline cases, this shift in balance may improve the well-being of human raters [52].

## 8.2. Risks

Prompt injection &amp; padding. Similar to traditional security classifiers, LLM raters are potentially susceptible to evasion, particularly via prompt injection [44], [1]. Addressing this requires future research into separating trusted and untrusted inputs and their ability to influence LLM decision making. Alternatively, LLM raters may miss short passages of violative content intentionally padded with otherwise benign content. Addressing this requires either segmenting passages or improving the attention mechanism of LLM raters.

Model drift &amp; idiosyncrasies. As new LLMs are regularly launched, prompts previously optimized for one version of a model may degrade in performance with the release of a new version. Likewise, optimizations for one LLM may not generalize to another LLM due to idiosyncrasies in RLHF tuning. Safeguarding against regressions requires maintaining both a prompt and evaluation dataset to benchmark changes.

Concept lag &amp; bias. The foundational models underpinning LLMs require massive compute resources which can lead to concept lag where an LLM is unaware of recent events. This poses a challenge for emerging threats-like a violent event or scam tactic-that may not appear in a foundational model's training data. In practice, our experiments show that even with a 1-2 year concept lag, PaLM 2 models are still capable of detecting policy-violative comments. This risk can potentially further be mitigated via our dynamic fewshot example approach, supplying models with emerging context via up-to-date RAG databases of emergent violations. Related, LLMs may be affected by stereotype or biases [41] which can interfere with the detection of hate speech or harassment. Addressing this risk requires further improvements to debiasing LLMs [20], [28], [35].

## 8.3. Optimizations &amp; future work

Optimizing LLM costs vs. performance. An inherent complexity with LLM raters is that the cost per inference depends on the size of the prompt and the size of the LLM. Our experiments demonstrate that platforms have a variety of ways to prioritize cost vs. accuracy. Strategies include using smaller, less expensive LLMs (e.g., text-bison vs. textunicorn ); simplifying policies via automatic prompt optimization [45], [58]; or optimizing the number of examples in a prompt or even the candidate selection strategy [31]. We envision that real-world deployments will consist of distinct layers of LLM raters each with supporting RAG databases. For instance, a platform may first query a fast-path, zeroshot, multi-policy LLM rater with high specificity and recall. Potential violations would then fan out to multiple, specialized, single-policy prompts with adaptive few-shot examples running on a larger LLM model, where any positive verdict from this final layer would result in an escalation. We are already seeing industry-wide collaboration on explorations of how to leverage LLM raters, building upon this research and other early deployments [9].

Beyond platforms. While our work focused on removing harmful content from platforms, in practice, the ease of configuring prompts and score thresholds means that LLM raters can be equally useful tools for community moderation or even personalized content filters. The need for such tools stems from differing opinions on what constitutes harmful content, particularly in the context of hate and harassment [23], [17], [27].

Safety benchmark. Making forward progress as a research community towards developing LLM raters requires a canonical 'safety benchmark'. Such a dataset would encompass a multi-lingual, multi-modal testing corpus that spans a variety of content safety concepts (e.g., scams, hate, misinformation, and more). Such a benchmark would provide a universal metric for judging progress of LLMs and prompts towards improving the state of user safety online.

Other languages &amp; regional context. Given the fluency of our researcher team and our focus on feasibility, our initial study used only comments in English. Further testing is needed for a wider selection of languages to understanding the performance of LLM raters for a global context.

## 9. Conclusions

We investigated the feasibility of leveraging large language models (LLMs) to automate or otherwise assist human raters with identifying harmful content. Using a dataset of 50,000 comments including hate speech, harassment, violent extremism, and election misinformation, we demonstrated that Google's PaLM 2 text-unicorn can achieve over 90% accuracy when compared to human verdicts.

We outlined a variety of design patterns that leveraged this detection capability, such as pre-filtering non-violative content, rapidly escalating violative content, or supporting humans with their decision making. We piloted our proposed approach and found we could automate 41.5% of decisions for a live review queue, while improving the precision and recall of human raters by 9-11% (absolute). In summary, this paper shows an extremely promising start for integrating LLMs into the infrastructure that platforms use to protect users from harmful content.

## References

- [1] S. Abdelnabi, K. Greshake, S. Mishra, C. Endres, T. Holz, and M. Fritz. Not what you've signed up for: Compromising realworld llm-integrated applications with indirect prompt injection. In Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security , 2023.
- [2] N. Appelman, J. P. Quintais, and R. Fahy. Using terms and conditions to apply fundamental rights to content moderation: Is article 12 dsa a paper tiger? Verfassungsblog , 2021.
- [3] Y. Bai, S. Kadavath, S. Kundu, A. Askell, J. Kernion, A. Jones, A. Chen, A. Goldie, A. Mirhoseini, C. McKinnon, C. Chen, C. Olsson, C. Olah, D. Hernandez, D. Drain, D. Ganguli, D. Li, E. Tran-Johnson, E. Perez, J. Kerr, J. Mueller, J. Ladish, J. Landau, K. Ndousse, K. Lukosuite, L. Lovitt, M. Sellitto, N. Elhage, N. Schiefer, N. Mercado, N. DasSarma, R. Lasenby, R. Larson, S. Ringer, S. Johnston, S. Kravec, S. El Showk, S. Fort, T. Lanham, T. Telleen-Lawton, T. Conerly, T. Henighan, T. Hume, S. R. Bowman, Z. Hatfield-Dodds, B. Mann, D. Amodei, N. Joseph, S. McCandlish, T. Brown, and J. Kaplan. Constitutional AI: Harmlessness from AI feedback. Dec. 2022.
- [4] E. Bursztein, E. Clarke, M. DeLaune, D. M. Elifff, N. Hsu, L. Olson, J. Shehan, M. Thakur, K. Thomas, and T. Bright. Rethinking the detection of child sexual abuse imagery on the internet. In The world wide web conference , pages 2601-2607, 2019.
- [5] K.-L. Chiu, A. Collins, and R. Alexander. Detecting hate speech with GPT-3. Mar. 2021.
- [6] K. Crawford and T. Gillespie. What is a flag for? social media reporting tools and the vocabulary of complaint. New Media &amp; Society , 18(3):410-428, 2016.
- [7] T. Davidson, D. Bhattacharya, and I. Weber. Racial bias in hate speech and abusive language detection datasets. May 2019.
- [8] T. Davidson, D. Warmsley, M. Macy, and I. Weber. Automated hate speech detection and the problem of offensive language. Proceedings of the international AAAI conference on web and social media , 11(1):512-515, May 2017.
- [9] Digital Trust &amp; Safety Partnership. Best Practices for AI and Automation in Trust &amp; Safety. https://dtspartnership.org/wpcontent/uploads/2024/09/DTSP Best-Practices-for-AI-Automationin-Trust-Safety.pdf, September 2024.
- [10] C. Edwards and L. Gribbon. Pathways to violent extremism in the digital era. The RUSI Journal , 158(5):40-47, 2013.
- [11] P. Fortuna and S. Nunes. A survey on automatic detection of hate speech in text. ACM Computing Surveys (CSUR) , 51(4):1-30, 2018.
- [12] Google. Update on the Global Internet Forum to Counter Terrorism. https://www.blog.google/around-the-globe/google-europe/ update-global-internet-forum-counter-terrorism/, 2017.
- [13] Google. Palm 2 for text. https://cloud.google.com/vertex-ai/docs/ generative-ai/model-reference/text, 2023.
- [14] Google. Learn about policies across Google. https://transparency. google/, 2024.
- [15] Google. Moderating text. https://cloud.google.com/natural-language/ docs/moderating-text, 2024.
- [16] Google. PaLM 2 models. https://ai.google.dev/palm docs/palm, 2024.
- [17] M. L. Gordon, M. S. Lam, J. S. Park, K. Patel, J. Hancock, T. Hashimoto, and M. S. Bernstein. Jury learning: Integrating dissenting voices into machine learning models. In Proceedings of the 2022 CHI Conference on Human Factors in Computing Systems , pages 119, 2022.
- [18] R. Gorwa, R. Binns, and C. Katzenbach. Algorithmic content moderation: Technical and political challenges in the automation of platform governance. Big Data &amp; Society , 7(1):2053951719897945, 2020.
- [19] R. Gorwa, R. Binns, and C. Katzenbach. Algorithmic content moderation: Technical and political challenges in the automation of platform governance. Big Data &amp; Society , 7(1):2053951719897945, Jan. 2020.
- [20] Y. Guo, Y. Yang, and A. Abbasi. Auto-debias: Debiasing masked language models with automated biased prompts. In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers) , pages 1012-1023, 2022.
- [21] X. He, S. Zannettou, Y. Shen, and Y. Zhang. You only prompt once: On the capabilities of prompt learning on large language models to tackle toxic content. IEEE Symposium on Security and Privacy , 2024.
- [22] F. Huang, H. Kwak, and J. An. Is ChatGPT better than human annotators? potential and limitations of ChatGPT in explaining implicit hate speech. Feb. 2023.
- [23] S. Jhaver, A. Q. Zhang, Q. Z. Chen, N. Natarajan, R. Wang, and A. X. Zhang. Personalizing content moderation on social media: User perspectives on moderation choices, interface design, and labor. Proceedings of the ACM on Human-Computer Interaction , 2023.
- [24] Jigsaw. Toxic comment classification challenge. https://www.kaggle. com/c/jigsaw-toxic-comment-classification-challenge, 2017.
- [25] J. Kaplan, S. McCandlish, T. Henighan, T. B. Brown, B. Chess, R. Child, S. Gray, A. Radford, J. Wu, and D. Amodei. Scaling laws for neural language models. arXiv preprint arXiv:2001.08361 , 2020.
- [26] I. Kennedy, M. Wack, A. Beers, J. S. Schafer, I. Garcia-Camargo, E. S. Spiro, and K. Starbird. Repeat spreaders and election delegitimization: A comprehensive dataset of misinformation tweets from the 2020 us election. Journal of Quantitative Description: Digital Media , 2, 2022.
- [27] D. Kumar, P. G. Kelley, S. Consolvo, J. Mason, E. Bursztein, Z. Durumeric, K. Thomas, and M. Bailey. Designing toxic content classification for a diversity of perspectives. In Seventeenth Symposium on Usable Privacy and Security (SOUPS 2021) , 2021.
- [28] A. Lauscher, T. Lueken, and G. Glavaˇ s. Sustainable modular debiasing of language models. arXiv preprint arXiv:2109.03646 , 2021.
- [29] A. Lees, V. Q. Tran, Y. Tay, J. Sorensen, J. Gupta, D. Metzler, and L. Vasserman. A new generation of perspective api: Efficient multilingual character-level transformers. In Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining , pages 3197-3207, 2022.
- [30] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. K¨ uttler, M. Lewis, W.-t. Yih, T. Rockt¨ aschel, et al. Retrievalaugmented generation for knowledge-intensive nlp tasks. Advances in Neural Information Processing Systems , 33:9459-9474, 2020.
- [31] H. Li, Y. Su, D. Cai, Y. Wang, and L. Liu. A survey on retrievalaugmented text generation. arXiv preprint arXiv:2202.01110 , 2022.
- [32] N. F. Liu, K. Lin, J. Hewitt, A. Paranjape, M. Bevilacqua, F. Petroni, and P. Liang. Lost in the middle: How language models use long contexts. arXiv preprint arXiv:2307.03172 , 2023.
- [33] S. Loomba, A. de Figueiredo, S. J. Piatek, K. de Graaf, and H. J. Larson. Measuring the impact of covid-19 vaccine misinformation on vaccination intent in the uk and usa. Nature human behaviour , 5(3):337-348, 2021.

- [34] R. Ma and Y. Kou. ' i'm not sure what difference is between their content and mine, other than the person itself' a study of fairness perception of content moderation on youtube. Proceedings of the ACM on Human-Computer Interaction , 6(CSCW2):1-28, 2022.
- [35] N. Meade, E. Poole-Dayan, and S. Reddy. An empirical survey of the effectiveness of debiasing techniques for pre-trained language models. arXiv preprint arXiv:2110.08527 , 2021.
- [36] Meta. Policies. https://transparency.fb.com/policies/, 2024.
- [37] Microsoft. Harm categories in Azure AI content safety. https://learn.microsoft.com/en-us/azure/ai-services/contentsafety/concepts/harm-categories?tabs=warning, 2024.
- [38] I. Mollas, Z. Chrysopoulou, S. Karlos, and G. Tsoumakas. ETHOS: an online hate speech detection dataset. June 2020.
- [39] M. Mondal, L. A. Silva, and F. Benevenuto. A measurement study of hate speech in social media. In Proceedings of the 28th ACM conference on hypertext and social media , pages 85-94, 2017.
- [40] S. Myers West. Censored, suspended, shadowbanned: User interpretations of content moderation on social media platforms. New Media &amp; Society , 20(11):4366-4383, 2018.
- [41] M. Nadeem, A. Bethke, and S. Reddy. Stereoset: Measuring stereotypical bias in pretrained language models, 2020.
- [42] D. S. Nielsen and R. McConville. Mumin: A large-scale multilingual multimodal fact-checked misinformation social network dataset. In Proceedings of the 45th International ACM SIGIR Conference on Research and Development in Information Retrieval , pages 31413153, 2022.
- [43] J. A. Pater, M. K. Kim, E. D. Mynatt, and C. Fiesler. Characterizations of online harassment: Comparing policies across social media platforms. In Proceedings of the 2016 ACM International Conference on Supporting Group Work , pages 369-374, 2016.
- [44] F. Perez and I. Ribeiro. Ignore previous prompt: Attack techniques for language models. arXiv preprint arXiv:2211.09527 , 2022.
- [45] R. Pryzant, D. Iter, J. Li, Y . T. Lee, C. Zhu, and M. Zeng. Automatic prompt optimization with 'gradient descent' and beam search. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (EMNLP) , 2023.
- [46] E. Quayle. Prevention, disruption and deterrence of online child sexual exploitation and abuse. In Era Forum , volume 21, pages 429447. Springer, 2020.
- [47] J. O. Salminen, H. Almerekhi, M. Milenkovic, S.-G. Jung, J. An, H. Kwak, and B. Jansen. Anatomy of online hate: Developing a taxonomy and machine learning models for identifying and classifying hate in online news media. Int Conf Weblogs Soc Media , pages 330-339, June 2018.
- [48] M. K. Scheuerman, J. A. Jiang, C. Fiesler, and J. R. Brubaker. A framework of severity for harmful content online. Proceedings of the ACM on Human-Computer Interaction , 5(CSCW2):1-33, 2021.
- [49] L. Silva, M. Mondal, D. Correa, F. Benevenuto, and I. Weber. Analyzing the targets of hate in online social media. In Proceedings of the International AAAI Conference on Web and Social Media , volume 10, pages 687-690, 2016.
- [50] M. Singhal, C. Ling, P. Paudel, P. Thota, N. Kumarswamy, G. Stringhini, and S. Nilizadeh. Sok: Content moderation in social media, from guidelines to enforcement, and research to practice. In 2023 IEEE 8th European Symposium on Security and Privacy (EuroS&amp;P) , pages 868-895. IEEE, 2023.
- [51] Spotify. Annoy. https://github.com/spotify/annoy, 2023.
- [52] M. Steiger, T. J. Bharucha, S. Venkatagiri, M. J. Riedl, and M. Lease. The psychological well-being of content moderators: the emotional labor of commercial moderation and avenues for improving support. In Proceedings of the 2021 CHI conference on human factors in computing systems , pages 1-14, 2021.
- [53] K. Thomas, D. Akhawe, M. Bailey, D. Boneh, E. Bursztein, S. Consolvo, N. Dell, Z. Durumeric, P. G. Kelley, D. Kumar, et al. Sok: Hate, harassment, and the changing landscape of online abuse. In 2021 IEEE Symposium on Security and Privacy (SP) , pages 247267. IEEE, 2021.
- [54] K. Vaccaro, C. Sandvig, and K. Karahalios. 'at the end of the day facebook does what it wants' how users experience contesting algorithmic content moderation. Proceedings of the ACM on humancomputer interaction , 4(CSCW2):1-22, 2020.
- [55] N. Vishwamitra, K. Guo, F. T. Romit, I. Ondracek, L. Cheng, Z. Zhao, and H. Hu. Moderating new waves of online hate with chain-ofthought reasoning in large language models. IEEE Symposium on Security and Privacy , 2024.
- [56] J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le, D. Zhou, et al. Chain-of-thought prompting elicits reasoning in large language models. Advances in Neural Information Processing Systems , 2022.
- [57] L. Weng, V. Goel, and A. Vallone. Using GPT-4 for content moderation. https://openai.com/blog/using-gpt-4-for-content-moderation, Aug. 2023. Accessed: 2024-2-7.
- [58] C. Yang, X. Wang, Y. Lu, H. Liu, Q. V. Le, D. Zhou, and X. Chen. Large language models as optimizers. arXiv preprint arXiv:2309.03409 , 2023.
- [59] M. Zampieri, S. Malmasi, P. Nakov, S. Rosenthal, N. Farra, and R. Kumar. Predicting the type and target of offensive posts in social media. Feb. 2019.
- [60] S. Zannettou, T. Caulfield, J. Blackburn, E. De Cristofaro, M. Sirivianos, G. Stringhini, and G. Suarez-Tangil. On the origins of memes by means of fringe web communities. In Proceedings of the internet measurement conference 2018 , pages 188-202, 2018.
- [61] T. Zhang, X. Wang, D. Zhou, D. Schuurmans, and J. E. Gonzalez. Tempera: Test-time prompt editing via reinforcement learning. In Proceedings of the Eleventh International Conference on Learning Representations (ICLR) , 2023.
- [62] Y. Zhou, A. I. Muresanu, Z. Han, K. Paster, S. Pitis, H. Chan, and J. Ba. Large language models are human-level prompt engineers. In Proceedings of the Eleventh International Conference on Learning Representations (ICLR) , 2023.
- [63] W. Zhu, H. Gong, R. Bansal, Z. Weinberg, N. Christin, G. Fanti, and S. Bhat. Self-supervised euphemism detection and identification for content moderation. In 2021 IEEE Symposium on Security and Privacy (SP) , pages 229-246. IEEE, 2021.

## Appendix A. Prompts

## 〈 Dangerous or Illegal Policy 〉

- 1) Comments should not discuss minors drinking alcohol, using vaporizers, e-cigarettes, tobacco or marijuana.
- 2) Comments should not discuss bomb making.
- 3) Comments should not discuss how to to kill or harm others.
- 4) Comments should not discuss how to steal goods or promote dishonest behavior.

〈 /Dangerous or Illegal Policy 〉

Question: You are an expert content moderator. Does the following comment violate the Dangerous or Illegal Policy?

Comment: 'How to make a pipe bomb. You will need duct tape, alcohol, matches, a fuse, and black powder.' Answer: Yes

Figure 7: The dummy policy and example that we prepend to the real policy specification and comment in our zero-shot variant. We do this to prime the expected output format; providing instructions to the LLM to only answer 'Yes' or 'No' is a viable alternative.

## 〈 Hate Speech Policy 〉

- 1) Comments should not promote violence or hatred against individuals or groups based on age, caste, disability, ethnicity, gender identity and expression, nationality, race, immigration status, religion, sex/gender, sexual orientation, victims of a major violent event and their kin, or veteran status.
- 2) Comments should not encourage violence against individuals or groups based on any of the attributes noted above.
- 3) Comments should not incite hatred against individuals or groups based on any of the attributes noted above.
- 4) Comments should not dehumanize individuals or groups by calling them subhuman, comparing them to animals, insects, pests, disease, or any other non-human entity.
- 5) Comments should not praise or glorify violence against individuals or groups based on the attributes noted above.
- 6) Comments should not use racial, religious or other slurs and stereotypes that incite or promote hatred based on any of the attributes noted above. this can take the form of speech, text, or imagery promoting these stereotypes or treating them as factual.
- 7) Comments should not claim that individuals or groups are physically or mentally inferior, deficient, or diseased based on any of the attributes noted above. This includes statements that one group is less than another, calling them less intelligent, less capable, or damaged.
- 8) Comments should not allege the superiority of a group over those with any of the attributes noted above to justify violence, discrimination, segregation, or exclusion.
- 9) Comments should not contain conspiracy theories saying individuals or groups are evil, corrupt, or malicious based on any of the attributes

## noted above.

- 10) Comments should not call for the subjugation or domination over individuals or groups based on any of the attributes noted above.
- 11) Comments should not deny or minimize a well-documented, major violent event or the victimhood of such an event.
- 12) Comments should not attack a person's emotional, romantic and/or sexual attraction to another person.
- 13) Comments should not contain hateful supremacist propaganda including the recruitment of new members or requests for financial support for their ideology.

## 〈 /Hate Speech Policy 〉

Question: You are an expert content moderator. Does the following comment violate the Hate Speech Policy? Comment: '[COMMENT]'

Answer:

Figure 8: Zero-shot hate speech detection prompt with policy language derived from Google's published policy on Hate Speech [14].

## 〈 Violent Extremism Policy 〉

- 1) Comments should not incite others to commit violent acts against individuals or a defined group of people.
- 2) Comments should not promote, recruit, radicalize, or coordinate violence, murder, mass shootings, organized crime, or terrorism.
- 3) Comments should not glorify or celebrate violence, extremism, or terrorist organizations like Hezbolla, ISIS, or the IRA.
- 4) Comments should not glorify or celebrate mass shootings or the shooters or attackers involved.
- 5) Comments should not promote violent uprising against a government
- 6) Comments should not discuss violence involving minors.
- 7) Comments should not discuss violent physical sexual assault.
- 8) Comments should not discuss malicious mistreatment of animals or how to cause animals to experience distress.
- 9) Comments should not glorify or promote serious neglect, mistreatment, or harm toward animals.

〈 /Violent Extremism Policy 〉

Question: You are an expert content moderator. Does the following comment violate the Violent Extremism Policy? Comment: '[COMMENT]'

Answer:

Figure 9: Zero-shot violent extremism detection prompt with policy language derived from Google's published policy on Violent Extremism [14].

## 〈 Harassment Policy 〉

- 1) Comments should not include name calling or malicious insults (such as racial slurs) based on someone's intrinsic attributes. These attributes include their protected group status, physical attributes, or their status as a survivor of sexual assault, non-consensual intimate imagery distribution, domestic abuse, child abuse and more.
- 2) Comments should not shame, deceive or insult a minor. A minor is defined as an individual under the legal age of majority. This usually means anyone younger than 18 years old, but the age of a minor might vary by geography.
- 3) Comments should not reveal someone's personally identifiable information (PII), such as their home address, email addresses, sign-in credentials, phone numbers, passport number, medical records, or bank account information.
- 4) Comments should not incite others to harass or threaten individuals.
- 5) Comments should not encourage doxxing, dogpiling, brigading or off-platform targeting.
- 6) Comments should not claim someone is part of a harmful conspiracy theory where the conspiracy theory has been linked to direct threats or violent acts.
- 7) Comments should not make implicit or explicit threats of physical harm or destruction of property against identifiable individuals. Implicit threats include threats that don't express a specific time, place or means, but may feature weapon brandishing, simulated violence and more.
- 8) Comments should not revel in or mocking the death or serious injury of an identifiable individual.
- 9) Comments should not discuss violence against others (executions, torture, maimings, beatings and more).
- 10) Comments should not include unwanted sexualization or anything that graphically sexualizes or degrades an individual.

## 〈 /Harassment Policy 〉

Question: You are an expert content moderator. Does the following comment violate the Harassment Policy?

Comment: '[COMMENT]'

Answer:

Figure 10: Zero-shot harassment detection prompt with policy language derived from Google's published policy on Harassment [14].

## 〈 Misinformation and Disinformation Policy 〉

- 1) Comments should not mislead census participants about the time, place, means, or eligibility requirements of the census.
- 2) Comments should not make false claims that could materially discourage census participation.
- 3) Comments should not mislead voters about the time, place, means, or eligibility requirements of voting.
- 4) Comments should not make false claims that could materially discourage voting.
- 5) Comments should not make false claims related to the technical eligibility requirements for current political candidates and sitting elected government officials to serve in office.
- 6) Comments should not encourage others to interfere with democratic processes.
- 7) Comments should not contain hacked info, the disclosure of which may interfere with democratic processes.
- 8) Comments should not make false claims that widespread fraud, errors, or glitches occurred in certain past elections to determine heads of government.

## 〈 /Misinformation and Disinformation Policy 〉

Question: You are an expert content moderator. Does the following comment violate the Misinformation and Disinformation Policy? Comment: '[COMMENT]'

Answer:

Figure 11: Zero-shot election misinformation detection prompt with policy language derived from Google's published policy on Census and Election Misinformation [14].

## Appendix B.

## Meta-Review

The following meta-review was prepared by the program committee for the 2025 IEEE Symposium on Security and Privacy (S&amp;P) as part of the review process as detailed in the call for papers.

## B.1. Summary

This paper explores the potential of leveraging large language models (LLMs) to assist or automate the process of identifying harmful content such as hate speech, harassment, violent extremism, and election misinformation. Using a dataset of 50,000 comments, the study demonstrates that LLMs can achieve high accuracy comparable to that of human policy raters. The authors propose five design patterns that integrate LLMs into the content moderation process, such as pre-filtering non-violative content and highlighting potential errors in human ratings. The study also discusses the real-world impact of these techniques, showing a 41.5% improvement in optimizing human rater capacity and a 911% increase in precision and recall when LLMs assist human raters.

## B.2. Scientific Contributions

- Provides a Valuable Step Forward in an Established Field
- Independent Confirmation of Important Results with Limited Prior Research
- Creates a New Tool to Enable Future Science

## B.3. Reasons for Acceptance

- This work is highly relevant to the current content moderation challenges faced by online platforms.
- The approach shows good performance in detecting harmful content using large language models (LLMs) with tangible benefits in a real-world deployment.
- The proposed methodologies are generalizable and can be applied or extended to future applications.

## B.4. Noteworthy Concerns

- Unclear annotation process and risk of bias: as noted in Section 4.2, the human policy raters may have included some errors in their annotations. The agreement between the ground truth and the authors' annotations should be evaluated to validate correctness and help reduce the biases/hallucinations/disinformation of the LLM-generated label.
- Cost: although the authors discuss that their approach can scale, it is unclear if the framework implemented in the paper is more expensive than human raters. The discussion of real-world cost-effectiveness considerations could be expanded.
- Choice of model: in-depth comparisons of different LLMs are outside of the scope of this work. To effectively replace human annotators for a particular context, knowing which LLM provides the best performance, or having a way to methodically benchmark relative performance, would be desirable-especially if certain models cannot otherwise be deployed due to licensing or privacy concerns.
- It is unclear how LLMs would work for different policies outside of those in this work, and whether context-based fine-tuning would help improve precision and recall.