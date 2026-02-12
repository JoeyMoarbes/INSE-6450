2024 6th International Conference on Data-driven Optimization of Complex Systems (DOCS)

## Large Language Model Assisted Adversarial Robustness Neural Architecture Search

| Rui Zhong ∗ , Yang Cao                                | Jun Yu                              | Masaharu Munetomo             |
|-------------------------------------------------------|-------------------------------------|-------------------------------|
| Graduate School of Information Science and Technology | Institute of Science and Technology | Information Initiative Center |
| Hokkaido University                                   | Niigata University                  | Hokkaido University           |
| Sapporo, Japan                                        | Niigata, Japan                      | Sapporo, Japan                |
| { rui.zhong.u5, yang.cao.y4 } @elms.hokudai.ac.jp     | yujun@ie.niigata-u.ac.jp            | munetomo@iic.hokudai.ac.jp    |

Abstract -Large Language Models (LLMs) have shown significant promise as evolutionary optimizers. This paper introduces a novel LLM-based Optimizer (LLMO) to address Neural Architecture Search Considering Adversarial Robustness (ARNAS), a classic combinatorial optimization problem. Using the standard CRISPE framework, we design the prompt and employ Gemini to iteratively refine solutions based on its responses. In our numerical experiments, we investigate the performance of LLMO on NAS-Bench-201-based ARNAS tasks with CIFAR-10 and CIFAR-100 datasets. The results, compared with six well-known metaheuristic algorithms (MHAs), highlight the superiority and competitiveness of using LLMs as combinatorial optimizers. The source code is available at https://github.com/RuiZhong961230/ LLMO.

Index Terms -Large Language Models (LLMs), Adversarial Attack, Neural Architecture Search (NAS), Combinatorial Optimizer

## I. INTRODUCTION

In recent years, the remarkable advancements in deep learning have been significantly affected and decelerated by the vulnerability of neural networks (NNs) to adversarial attacks [1]. These attacks, which involve imperceptible perturbations to input data, can lead to highly incorrect predictions [2]. Consequently, the deployment and configuration of NNs in security-critical applications face serious challenges [3]. As the complexity of these attacks continues to evolve, the imperative to develop robust neural architectures has never been more pressing.

In the meantime, neural architecture search (NAS) has emerged as a promising and powerful tool for the automatic design of neural networks. This technique aims to identify optimal architectures that meet specified performance criteria. However, traditional NAS methods focus primarily on mainstream metrics like accuracy, latency, and model size while the negative effects caused by the adversarial attack are commonly neglected [4]. Therefore, in the rapid development of the artificial intelligence (AI) community, the adversarial robustness of designed NNs should be considered as a crucial factor, that advances adversarial robustness NAS (ARNAS) techniques.

Although ARNAS tasks are significantly more complex and challenging than traditional NAS tasks, they are fundamentally combinatorial optimization problems. These can be effectively addressed by approximation optimizers with limited CPU time [5]. Meanwhile, large language models (LLMs), such as Gemini, GPT, and LLaMA, have demonstrated exceptional capabilities in understanding and generating human-like text, solving complex problems, and supporting various domains in AI research [6]. The potential of LLMs as optimizers has also been explored: Yang et al. [7] proposed Optimization by PROmpting (OPRO), where the traveling salesman problem (TSP) is described in natural language and used as input for the LLM to generate new solutions. Liu et al. [8] introduced LLM-driven EA (LMEA), which uses LLMs as evolutionary combinatorial optimizers with minimal domain knowledge and no additional training required. In LMEA, the LLM selects parent solutions from the current population in each generation, applies search operators to generate offspring, and employs a self-adaptive selection mechanism to ensure the survival of elite solutions. Given these findings, the motivation of this study is to utilize LLMs as combinatorial optimizers to solve ARNAS tasks, potentially accelerating optimization convergence in the search for ARNAS.

This paper proposes a novel LLM-based Optimizer (LLMO) for addressing ARNAS tasks. We instruct the LLM Gemini to iteratively search for the optimal architecture under adversarial attacks with the standard CRISPE framework. Numerical experiments on ARNAS tasks [9] were conducted, comparing LLMO with six well-known MHAs. The experimental results demonstrate the feasibility and effectiveness of LLMO

The rest of this paper is organized as follows. Section II introduces the related works including the CRISPE framework and ARNAS. Section III details our proposed LLMO, Section IV describes experimental settings and results, we analyze the performance of LLMO in Section V, and finally, Section VI concludes our work.

## II. RELATED WORKS

## A. CRISPE framework

Many researchers have recognized the crucial role of prompts in guiding LLMs to produce satisfactory responses [10]. Consequently, prompt engineering has rapidly emerged as an essential discipline, leading to the development of various techniques such as zero-shot, one-shot, few-shot prompt-

ing, and chain-of-thought prompting. This paper adopts the CRISPE framework, a structured prompt engineering approach, to design effective prompts. Here, Fig. 1 presents the components in the CRISPE framework.

Fig. 1: Components in the CRISPE framework.

<!-- image -->

## B. Adversarial robustness neural architecture search (ARNAS)

The ARNAS instances presented in [9] are employed as the benchmark suite in this study, where the structures are demonstrated in Fig. 2. A cell in Fig. 2 consists of four nodes (i.e., feature maps) and six edges (i.e., possible operations). Available operations contain 1x1 convolutions, 3x3 convolutions, 3x3 average pooling, skip connection, and zeroize connection. Consequently, the possible combinations of potential architectures are 5 6 = 15 , 625 , among them 6 , 466 architectures are non-isomorphic.

Here, four representative adversarial attack methods are adopted: the fast gradient sign method (FGSM) [11], projected gradient descent (PGD) [12], adaptive PGD (APGD) [9], and square attack [9]. Detailed descriptions of these methods can be found in corresponding papers.

## III. OUR PROPOSAL: LLMO

A demonstration of the proposed LLMO is presented in Fig. 3. In the initial step, we design and input the prompt using the CRISPE framework into Gemini. The response from Gemini is then refined as a solution to the ARNAS instance. We utilize the prediction accuracy of the feedback to automatically update the prompt. These processes are repeated until the optimization is complete.

Additionally, the overview of the designed prompt is summarized as follows. The contents within ' {} ' in the prompt will be replaced by the real data during optimization.

- CR: Act as a combinatorial optimizer for adversarial robustness neural architecture search.
- I: The objective of this task is to maximize the accuracy.
- S: There are { number of operations } possible operations and { number of edges } edges that need to be deployed.

You need to specify a { number of edges } -bit array where the value in each index is an integer within [0, { number of operations } ). The current best solution is { best solution } with the best accuracy { best accuracy } .

- P: Not applicable.
- E: Give me one solution in the array-like format.

The pseudocode of the proposed LLMO is presented in Algorithm 1. The proposed LLMO offers a significant design advantage: users do not need to understand the working mechanism of Gemini or the specific design of search operators. This means that even amateurs with no prior knowledge of evolutionary computation (EC) and ARNAS can easily use LLMO for optimization. This user-friendly approach ensures easy implementation and accessibility.

## Algorithm 1 LLMO

## Require: Max. iteration: T

Ensure: Optimum: x t best

- 2: Evaluate x t best by ARNAS instance
- 1: Randomly initialize the solution x t best
- 3: t = 0
- 4: while t &lt; T do
- 5: Construct prompt using CRISPE framework
- 6: Input prompt to Gemini
- 7: Check the feasibility of the responded solution
- 8: Update the current best solution x t best
- 9: t ← t +1
- 10: end while
- 11: return x t best

## IV. NUMERICAL EXPERIMENTS

This section introduces the numerical experiments on ARNAS instances to investigate the performance of LLMO competing with well-known MHAs. Section IV-A presents the detailed experimental settings and Section IV-B summarizes the detailed experimental results.

## A. Experimental settings

Six metaheuristic algorithms (MHAs) are employed as competitor algorithms: GA [13], PSO [14], DE [15], CMA-ES [16], JADE [17], and success-history-adaptive DE (SHADE) [18]. The parameters of these algorithms are summarized in Table I. The population size of competitor algorithms is fixed at 30 while LLMO is a single solution based optimization approach. The maximum fitness evaluation (FE) of all optimizers is fixed at 30 and 3000, respectively. To alleviate the effect of randomness, each algorithm is implemented in 30 trial runs.

## B. Experimental results

The experimental results are summarized in Table II, and the convergence curves are in Figs. 4 and 5.

<!-- image -->

Fig. 2: The architecture of NAS-Bench-201-based ARNAS search space.

Fig. 3: A demonstration of LLMO.

<!-- image -->

Fig. 4: Convergence curves of optimizers for ARNAS on CIFAR-10.

<!-- image -->

Fig. 5: Convergence curves of optimizers for ARNAS on CIFAR-100.

<!-- image -->

TABLE I: The parameters of competitor algorithms.

| Algorithms   | Parameters                                                    | Value                        |
|--------------|---------------------------------------------------------------|------------------------------|
| GA           | crossover probability pc mutation probability pm selection    | 0.9 0.01 tournament          |
| PSO          | inertia factor w coefficients c 1 and c 2 max. and min. speed | 1 2.05 2 and -2              |
| DE           | mutation strategy scaling factor F crossover rate Cr          | DE/cur-to-rand/1/bin 0.8 0.9 |
| CMA-ES       | σ                                                             | 1.3                          |
| JADE         | µ F and µ Cr                                                  | 0.5 and 0.5                  |
| SHADE        | µ F and µ Cr                                                  | 0.5 and 0.5                  |

## V. DISCUSSION

The experimental results presented in Table II and Fig. 4 confirm the competitiveness of LLMO, particularly in NAS without adversarial attacks and ARNAS with FGSM attacks in both CIFAR-10 and CIFAR-100 datasets. In these four instances, our proposed LLMO outperforms the competitor algorithms, demonstrating the potential and effectiveness of LLM as an optimizer.

Additionally, while GA was originally designed for binary optimization problems, and PSO, DE, CMA-ES, JADE, and SHADE were designed for continuous optimization problems, these algorithms require transfer functions to convert the search domain. The use of transfer functions can lead to different solutions in the original search domain being mapped to identical solutions in the transferred search domain, which deteriorates the quality of constructed offspring individuals and reduces search efficiency. However, this issue does not exist in the proposed LLMO. In the prompt design, the constructed offspring individuals are directly encoded as a number of edges-bit array, where the value in each index is an integer within [0, number of operations). This direct encoding method for the generation of offspring individuals is more efficient than the approach used by MHAs that rely on transfer functions.

Furthermore, this research reveals the potential of LLMO in solving combinatorial optimization problems, and we believe that it can further adapt to various combinatorial domains such as feature selection [19], job scheduling [20], and portfolio management problems [21].

## VI. CONCLUSION

Motivated by the ability of LLMs to solve combinatorial optimization problems such as TSP, this paper proposes a novel LLM-based optimizer (LLMO) to address adversarial robustness neural architecture search (ARNAS) tasks. We design the prompt using the standard CRISPE framework and iteratively refine it during optimization. The experimental results confirm the competitiveness of LLMO and highlight the potential of LLMs as effective optimizers for solving combinatorial optimization problems.

In future research, we will continue to explore the optimization capacity of LLMs in various optimization domains.

TABLE II: Results of prediction accuracy in the ARNAS benchmark.

| Prob.     | Prob.   |    GA |   PSO |    DE |   CMA-ES |   JADE |   SHADE |   LLMO |
|-----------|---------|-------|-------|-------|----------|--------|---------|--------|
|           | Clean   | 94.14 | 94.34 | 94.26 |    94.33 |  94.42 |   94.33 |  94.44 |
|           | FGSM    | 66.7  | 68.07 | 67.88 |    67.62 |  68    |   67.76 |  68.35 |
| CIFAR-10  | PGD     | 57.01 | 58.37 | 58.04 |    58.32 |  58.42 |   58.46 |  58.6  |
| CIFAR-10  | APGD    | 52.91 | 53.43 | 52.86 |    53.25 |  53.5  |   53.49 |  53.47 |
| CIFAR-10  | Squares | 70.78 | 72.56 | 71.65 |    71.37 |  72.24 |   72    |  72.17 |
|           | Clean   | 72.42 | 73.23 | 72.73 |    73.13 |  73.17 |   73.33 |  73.33 |
|           | FGSM    | 27.99 | 28.68 | 28.11 |    28.42 |  28.48 |   28.5  |  28.78 |
| CIFAR-100 | PGD     | 28.39 | 28.76 | 28.73 |    28.63 |  28.8  |   28.8  |  28.67 |
| CIFAR-100 | APGD    | 25.8  | 25.98 | 25.92 |    25.93 |  25.9  |   26.02 |  25.94 |
| CIFAR-100 | Squares | 37.21 | 39.66 | 37.2  |    38.64 |  38.74 |   38.88 |  38.66 |

## ACKNOWLEDGEMENT

This work was supported by JSPS KAKENHI Grant Number 21A402 and 24K15098 and JST SPRING Grant Number JPMJSP2119.

## REFERENCES

- [1] J. Liu, R. Cheng, and Y. Jin, 'Bi-fidelity evolutionary multiobjective search for adversarially robust deep neural architectures,' Neurocomputing , vol. 550, p. 126465, 2023.
- [2] S. Huang, Z. Lu, K. Deb, and V. N. Boddeti, 'Revisiting residual networks for adversarial robustness,' in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) , June 2023, pp. 8202-8211.
- [3] J. Su, D. V. Vargas, and K. Sakurai, 'One pixel attack for fooling deep neural networks,' IEEE Transactions on Evolutionary Computation , vol. 23, no. 5, pp. 828-841, 2019.
- [4] L. Bortolussi, G. Carbone, L. Laurenti, A. Patane, G. Sanguinetti, and M. Wicker, 'On the robustness of bayesian neural networks to adversarial attacks,' IEEE Transactions on Neural Networks and Learning Systems , pp. 1-14, 2024.
- [5] R. Zhong, Y. Xu, C. Zhang, and J. Yu, 'Efficient multiplayer battle game optimizer for adversarial robust neural architecture search,' 2024.
- [6] R. Zhong, Y. Xu, C. Zhang, and J. Yu, 'Leveraging large language model to generate a novel metaheuristic algorithm with crispe framework,' Cluster Computing , pp. 1-35, 2024.
- [7] C. Yang, X. Wang, Y. Lu, H. Liu, Q. V. Le, D. Zhou, and X. Chen, 'Large language models as optimizers,' 2024.
- [8] S. Liu, C. Chen, X. Qu, K. Tang, and Y.-S. Ong, 'Large language models as evolutionary optimizers,' 2024.
- [9] S. Jung, J. Lukasik, and M. Keuper, 'Neural architecture design and robustness: A dataset,' in ICLR , 2023.
- [10] J. White, Q. Fu, S. Hays, M. Sandborn, C. Olea, H. Gilbert, A. Elnashar, J. Spencer-Smith, and D. C. Schmidt, 'A prompt pattern catalog to enhance prompt engineering with chatgpt,' 2023.
- [11] I. J. Goodfellow, J. Shlens, and C. Szegedy, 'Explaining and harnessing adversarial examples,' 2015.
- [12] A. Kurakin, I. Goodfellow, and S. Bengio, 'Adversarial machine learning at scale,' 2017.
- [13] J. H. Holland, 'Genetic algorithms,' Scientific American , vol. 267, no. 1, pp. 66-73, 1992.
- [14] J. Kennedy and R. Eberhart, 'Particle swarm optimization,' in Proceedings of ICNN'95 - International Conference on Neural Networks , vol. 4, 1995, pp. 1942-1948 vol.4.
- [15] R. Storn, 'On the usage of differential evolution for function optimization,' in Proceedings of North American Fuzzy Information Processing , 1996, pp. 519-523.
- [16] N. Hansen, S. D. M¨ uller, and P. Koumoutsakos, 'Reducing the time complexity of the derandomized evolution strategy with covariance matrix adaptation (cma-es),' Evolutionary Computation , vol. 11, no. 1, pp. 1-18, 2003.
- [17] J. Zhang and A. C. Sanderson, 'Jade: Adaptive differential evolution with optional external archive,' IEEE Transactions on Evolutionary Computation , vol. 13, no. 5, pp. 945-958, 2009.
- [18] R. Tanabe and A. Fukunaga, 'Success-history based parameter adaptation for differential evolution,' in 2013 IEEE Congress on Evolutionary Computation , 2013, pp. 71-78.
- [19] R. Zhong, C. Zhang, and J. Yu, 'Chaotic vegetation evolution: leveraging multiple seeding strategies and a mutation module for global optimization problems,' Evolutionary Intelligence , pp. 1-25, 01 2024.
- [20] M. Xu, Y. Mei, F. Zhang, and M. Zhang, 'Niching genetic programming to learn actions for deep reinforcement learning in dynamic flexible scheduling,' IEEE Transactions on Evolutionary Computation , pp. 1-1, 2024.
- [21] Y. Ma, W. Wang, and Q. Ma, 'A novel prediction based portfolio optimization model using deep learning,' Computers &amp; Industrial Engineering , vol. 177, p. 109023, 2023.