## Language Model Agnostic Gray-Box Adversarial Attack on Image Captioning

Nayyer Aafaq , Naveed Akhtar , Member, IEEE , Wei Liu, Mubarak Shah , Life Fellow, IEEE

, and Ajmal Mian , Senior Member, IEEE

Abstract -Adversarial susceptibility of neural image captioning is still under-explored due to the complex multi-model nature of the task. We introduce a GAN-based adversarial attack to effectively fool encoder-decoder based image captioning frameworks. Unique to our attack is the systematic disruption of the internal representation of an image at the encoder stage which allows control over the captions generated at the decoder stage. We cause the desired disruption with an input perturbation that promotes similarity between the features of the input image with a target image of our choice. The target image provides a convenient handle to control the incorrect captions in our method. We do not assume any knowledge of the decoder module, which makes our attack 'gray-box'. Moreover, our attack remains agnostic to the type of decoder module, thereby proving effective for RNNs as well as Transformers as the language models. This makes our attack highly pragmatic.

the same line, we explore the adversarial susceptibility of language-and-vision system in the context of encoder-decoder scheme for image captioning.

Index Terms -Adversarial attack, image captioning, recurrent networks, transformers, language models, generative adversarial networks (GANs).

## I. INTRODUCTION

R ECENT studies have unearthed a multitude of adversarial attacks that can fool deep learning [1]. These attacks mainly focus on the problem of image classification [2], [3], [4], [5]. Nevertheless, there has been an increasing interest in the research community to also explore adversarial attacks against more complex vision systems [6], [7], [8]. Along

Manuscript received 20 December 2021; revised 1 July 2022 and 23 November 2022; accepted 23 November 2022. Date of publication 5 December 2022; date of current version 19 December 2022. This work was supported in part by the Australian Research Council (ARC) Discovery under Project DP190102443 and in part by the Defense Advanced Research Projects Agency (DARPA) under Agreement HR00112090095. The work of Naveed Akhtar was supported by the Office of National Intelligence, National Intelligence Post-Doctoral funded by the Australian Government under Grant NIPG-2021-001. The work of Ajmal Mian was supported by the Australian Research Council Future Fellowship Award funded by the Australian Government under Project FT210100268. The associate editor coordinating the review of this manuscript and approving it for publication was Dr. Patrick Bas. (Corresponding author: Nayyer Aafaq.)

Nayyer Aafaq was with the Department of Computer Science and Software Engineering, The University of Western Australia, Crawley, WA 6009, Australia. He is now with the College of Aeronautical Engineering, National University of Sciences and Technology (NUST), Islamabad 44000, Pakistan (e-mail: nayyer.aafaq@research.uwa.edu.au).

Naveed Akhtar, Wei Liu, and Ajmal Mian are with the Department of Computer Science and Software Engineering, The University of Western Australia, Crawley, WA 6009, Australia (e-mail: naveed.akhtar@ uwa.edu.au; wei.liu@uwa.edu.au; ajmal.mian@uwa.edu.au).

Mubarak Shah is with the Center for Research in Computer Vision (CRCV), University of Central Florida, Orlando, FL 32816 USA (e-mail: shah@crcv.ucf.edu).

Digital Object Identifier 10.1109/TIFS.2022.3226905

As compared to classification, image captioning offers two unique challenges for computing adversarial examples. Firstly, it is not straightforward to extend the notion of 'adversarial' examples to the problem of image captioning. Classifiers map an image to a discrete label. Changing this mapping to an incorrect label, makes the input adversarial. An analogous understanding of 'adversarial' input for captioning problem requires discretization of the solution space. This makes the search space for the underlying mapping overwhelmingly large, as the same information can be expressed in a number of different captions while still being correct. Secondly, attacks on classifiers are aimed to fool a single model. However, captioning is a multi-model problem that involves visual and language modules. Whereas attacks on visual models ( e . g ., CNNs) are well-studied, adversarial susceptibility of language modules is yet to be thoroughly explored, leaving alone the specific challenges of a 'multi-model' problem in captioning.

The first attempt to attack a captioning framework was made by Xu et al. [11]. Their approach treats the output caption as a single label, thereby focusing on fooling the decoder ( i . e ., RNN) of the framework while keeping the CNN embeddings unchanged. The 'Show and Fool' [12] method introduced the notions of 'targeted caption' and 'targeted keyword' in the context of adversarial attacks on captioning frameworks. Recently, [13] proposed a more restricted targeted partial captions attack to enforce targeted keywords to occur at a specific location in the caption. All these methods must know the optimization objective of the language model to generate the adversarial examples. While useful, this scheme requires the complete knowledge of the captioning framework to fool it. Moreover, it requires computing the adversarial samples anew if the visual model in the framework is replaced. Considering that captioning methods frequently rely on a variety of off-the-shelf visual models, this is undesirable.

In this work, we propose to perturb the image based on the internal representation of the visual model used in the captioning framework. This allows us to effectively control the image caption without requiring the knowledge of the language model, which is more practical (see Fig. 1). Our attack alters the image such that the internal representation of the visual

1556-6021 ' 2022 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission.

See https://www.ieee.org/publications/rights/index.html for more information.

Fig. 1. Example of adversarial attack crafted by our technique. (a) Show-andTell [9] model that employs LSTM as language model. (b) Show-Attend-andTell [10] model that additionally uses attention mechanism. (c) Transformer used as language model. Target caption is shown in red. We see that the predicted captions by all three models are relevant to the target caption. M denotes the Meteor score between target and respective predicted caption. In our experiments, we categorise all the results with Meteor score under 0 . 15 ( i . e ., threshold τ ) as failed attempts.

<!-- image -->

classifier gets drastically changed for the image with minimal image-space perturbations. Since the language model depends strongly on the internal representation of the visual model, this allows us to control the subsequent caption without any knowledge of the language model. To generate the adversarial images, we propose a GAN-based method that alters the representation of the desired internal layer for the image. The generator is trained to compute the perturbation that results in pronounced image features of the target (incorrect) class and suppressed features of the source (correct) class. The source and target classes can be pre-selected in our attack. The GAN-based setup provides our attack the advantage that the perturbation is computed with a single forward pass for a deployed model, unlike the typical iterative methods that are more time consuming due to iterative computations.

We summarise the main contributions of our work as follows.

- We propose a GAN-based attack on image captioning framework that is able to alter the internal representation of the image to control the captions generated by the subsequent language model. This is the first study that performs adversarial attacks on image captioning systems via visual encoder only.
- We demonstrate that the captioning frameworks can be fooled with much higher success rates when attacked on the internal layers of the visual models instead of the classification layer.
- Extensive experiments show that state-of-the-art image captioning models can be fooled by the proposed method with high success rate.
- Lastly, we explore the workings of internal mechanism of the captioning framework via adversarial attack.

## II. RELATED WORK

We first review related work in visual ( i . e ., image and video) captioning followed by adversarial attacks on the visual tasks. Next, we discuss the existing line of work on adversarial attacks on captioning frameworks.

## A. Visual Captioning

Visual captioning is a multi-modal problem which has recently gained a surge of interest, primarily due to the advancement in deep learning [14], availability of large scale datasets [15], [16], [17], [18] and computational capability enhancement of machines. Visual captioning includes image captioning [19], [20], [21], video captioning [22], [23], [24], [25], and dense image/video captioning [17], [26]. Most visual captioning approaches adopt encoder-decoder architecture. The encoder extracts features from the input image/video. For that matter pre-trained deep neural models ( i . e ., CNNs) are used as encoders in the captioning framework. Subsequently, recurrent networks [27], [28] or transformers [29] are employed to decode the visual features into natural language sentences. More recent methods augment this scheme with advanced concepts of e . g ., reinforcement learning [30], objects and actions modeling [19], [31], [32], incorporating fourier transform with CNN [23], attention mechanism [10], [33], [34], semantic attribute learning [35], [36], multimodal memory [37], [38] and audio integration [39], [40] for improved performance. Goal of dense image captioning [41] is to densely detect visual concepts from images, describing each with a short phrase. Compared to images, video generally contains rich information with multiple events, which is hard to describe using a single sentence. Therefore, few recent works [42] and [43] proposed to generate multiple sentences ( i . e ., paragraph) to describe video contents in detail. The work is further extended to dense video captioning [17] which aims to detect and describe multiple events in long untrimmed videos. In this, all the detected events are described where each sentence describe a specific event in the video.

## B. Adversarial Examples

Where deep learning has proposed solutions to several complex problems, it has been proven that it is vulnerable to adversarial examples [44]. Depending on the available information about the target model, contemporary works can be classified into three main categories i . e ., white-box , gray-box and black-box attacks. We refer the readers to [1] for more details. Deep networks have performed really well on visual tasks e . g ., image classification [45], object detection and semantic segmentation [46], [47], sometimes even surpassing human performance. Primarily due to this fact, most existing works on adversarial attacks study the robustness of deep models for these tasks. For instance, for image classification,

many techniques have been proposed for computing adversarial examples; e . g . Fast Gradient Sign Method (FGSM) [5], Iterative Fast Gradient Sign Method (I-FGSM) [48], optimisation based methods Carlini and Wager attack [49], boxconstrained L-BFGS [44], DeepFool [50] and others. These methods demonstrate that CNN-based visual classifiers can be easily fooled with adversarial examples. Among such methods, one particularly relevant group develops transferable attacks on classifiers that leverage the internal representation of models to improve attack transferability [51], [52], [53]. Though restricted to the classification task, these technique bear conceptual similarity to our method in terms of dealing with internal representations instead of class labels to compute the adversarial signal. Along with classifiers, other CNN-based visual models, e . g ., object detection and semantic segmentation, have also been demonstrated to be susceptible to adversarial attacks [8], [54], [55], [56].

It is easy to see that all the aforementioned methods share the same trait that they target CNN models for classification, which are differentiable programs. Hence, their loss function gradients with respect to the input image can easily be computed with backpropagation to generate adversarial examples. Different from CNNs, another line of works explore the adversarial examples for recurrent neural networks for text processing [57], [58] and deep reinforcement learning [59], [60], [61]. There, the backpropagation of gradients and model's fooling objective become more complicated due to the underlying architecture and objectives of the original models. In our work, we study the adversarial examples for image captioning framework i . e ., vision-language model that faces the challenges fooling both CNNs and language models.

## C. Adversarial Examples for Captioning

Most of the contemporary captioning frameworks are composed of CNN followed by language models ( i . e ., RNNs or transformers). Pre-trained CNNs are used to extract features from the visual input. The extracted features from a selected hidden layer of the CNN are then fed to the language model to generate natural language description for the visual input. In contrast to CNNs, the language model in the captioning framework carries additional temporal dependency in the generated output i . e ., words. Due to the temporal relationship among the generated words, it is much more challenging to compute the desired (adversarial) gradients for the overall framework. Xu et al. [11], are the first to attempt an attack on captioning framework. In their approach, they treated the output sentences as a single label, thereby altering complete sentences. Moreover, they focused on generating adversarial examples to fool the RNN part of the model, while retaining the original CNN embeddings.

The 'Show and Fool' [12] method proposed 'targeted captions' and 'targeted keywords' attacks on the captioning framework. The attack of targeted captions generate complete captions for the input image. In its 'targeted keywords' attack, the predicted sentence should include the targeted keywords. Recently, [13] proposed more restricted targeted partial captions attack that can enforce the targeted keywords to occur at specific locations. These methods leverage from language model objective functions to generate the adversarial examples. Though successful, this scheme requires complete model information of the framework for successful fooling which is often not practical. 'Mimic and Fool' [62] proposed to construct a noise image that can mimic the features of the original image. However, this is not a practical attack as it fails to maintain the imperceptibility. Another variant of the attack i . e ., one image many outputs (OIMO) address the issue by adding a fixed noise to the original image. Both of these variants are iterative methods and are image specific. In contrast, the proposed is a learning based technique that requires a single forward pass at the test time which makes it efficient, and hence more practical. Moreover, proposed technique is able to generate image-agnostic perturbations that remain valid for all the images of the same class.

## III. METHODOLOGY

## A. Problem Formulation

Before articulating our methodology, we first briefly touch the generic strategy of adversarial attack for classification models, explaining how is this different from the adversarial attack on a captioning framework. Let I ∈ R m be a sample of a distribution I over the natural images and φθ ( I ) be a deep visual classification model that maps I to its correct label y . The common aim of generating perturbations in adversarial settings is to compute p ∈ R m that satisfies the constraint

<!-- formula-not-decoded -->

where y and ˆ y denote the true and incorrect labels respectively, || . || p denotes the /lscript p norm that is constrained by η in the optimization problem. Here, restricting ˆ y to a pre-defined label results in a targeted adversarial attack.

For a given captioning framework, the targeted caption is denoted by

<!-- formula-not-decoded -->

where S indicates the words in vocabulary V with S 1 and SN represent the start and end of caption symbols, and N is the caption length. Note that while N is variable, it does not exceed a pre-defined maximum length of the caption. The posterior probability of the caption is computed as

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where I represents the benign image and p shows the perturbations. To predict the targeted caption S , captioning systems need to maximize the probability of the caption S conditioned on the image I + p among all possible captions set /Psi1 , i . e .,

In captioning frameworks, the probability is usually computed by RNN cell ϕ , with its hidden state hq -1 and input word Sq -1

<!-- formula-not-decoded -->

Fig. 2. Proposed Methodology : Overall architecture for generating adversarial examples for image captioning framework. A fixed pattern sampled from a uniform distribution i . e ., n ∈ R m is passed through the generator. The generator output is added to the source image i . e ., I s and the scaled result is passed through the discriminator to get the deep representation v gs at the desired j th layer. Similarly, target image i . e ., I t is passed through the discriminator to get v t . Discriminator computes and back-propagates the gradients to update the input image I ′ gs . After re-scaling and subtracting the original image, updated perturbations I ′ g are separated and generator gradients are updated. The output of the trained generator is then added to the source image to generate the captions similar to the target image caption.

<!-- image -->

where zq represents a vector of logits for every possible word in the vocabulary V . Most existing methods try to maximize the captions probabilities by directly using its negative log probabilities as a loss where as the RNN cell hidden state at q th time step is initialised with hq -1 from the CNN model. For the CNN model here, an existing pretrained model e . g ., ResNet-152 is employed. In the captioning models, the CNN is not trained but for a given input image, one may compute perturbations by backpropagating error from the RNN to the CNN input. This operation must be repeated for all time steps to allow the RNN to update weights using backpropagation through time (BPTT) across a sequence of the internal vector representations of input images. Another possibility is to fool the captioning framework by employing a classification-base attack on the CNN model and then feeding the perturbed image hidden state to the language model ( i . e ., RNN or Transformer). However, as language model uses the hidden state from deep CNN, and not the classification layer logits, this simple strategy is ineffective.

Intuitively, there is a single pre-trained CNN model and a Transformer or sequence of RNN models, one for each time step. We want to apply the perturbations to the CNN model and pass on the output of each input image to the subsequent language model as a single time step. For that matter, rather than manipulating the class label of the image, we manipulate the internal representation of the CNN φθ (.) to conduct fooling of the captioning framework. This allows us to compute the perturbations independently of the language model stage of the framework.

Let φ j ( I ) be the activations of the j th layer of the classification network φ when processing an image I . We formulate the feature reconstruction loss as the squared normalized Euclidean distance between the feature representations

<!-- formula-not-decoded -->

As demonstrated in [63], finding an image ˆ y that minimizes the feature reconstruction loss for early layers tends to produce images that are visually indistinguishable from y . As we reconstruct the image from higher layers, image content and overall spatial structure are preserved. Using a feature reconstruction loss for training our generator network encourages the source image I s to produce similar internal representations as of the target image I t . Our objective is to reconstruct the adversarial image with a learning-based technique under a GAN framework. A generator model can produce the adversarial samples on-the-fly once it has been successfully trained. From an adversarial perspective, this is more practical as compared to iterative methods, e.g., [64], [65], that require multiple iterations to compute the desired perturbations during test time. Moreover, due the complex nature of our underlying gray-box settings, a learning-based method is expected to better account for the challenges of our problem as compared to the heuristic iterative algorithms.

## B. Computing Generative Perturbations

To compute our adversarial perturbations, we sample a fixed pattern Z ∈ [ 0 , 1 ] n from a uniform distribution U [ 0 , 1 ] n . This sample is fed to the generator G θ to compute the perturbation. The output of the generator G θ ( Z ) is first scaled to have a fixed norm. Henceforth, we denote the generator output as Ig for brevity. The scaled output is then added to the source image, producing Igs with the aim to bring the internal layer features of the image close to the target image It , see Fig. 2. This means, that the language model in turn will generate the same captions as for the target image despite the fact that the two images are altogether different. The target image is selected based upon dissimilarity to the source class using a simple strategy of picking a random image from the class that has the least probability when the source image is classified by the CNN-based encoder.. In this way, we can control the output of the language model without any information about the model.

TABLE I

## SUMMARY OF SYMBOLS AND NOTATIONS USED IN THE TEXT

The discriminator forms the second part of our overall GAN setup. Before feeding both images to the discriminator, we clip them to keep them in the valid dynamic range of the images on which the discriminator is trained. We feed the clipped images Igs and It to the discriminator network D to obtain the output feature vectors i . e ., v gs and v t of the j th layer of the discriminator. We employ a pre-trained CNN as the discriminator in our approach. We remove the undesired classification layers to obtain the desired i . e ., j th layer features as output such that;

are seeking to synthesize, 299 × 299 × 3. After each transposed convolution layer, we apply batch normalization and the Leaky ReLU activation function. At the final layer, we do not apply batch normalization and, instead of ReLU , we use the tanh activation function. We can summarise all the steps as follows :

- We take a uniform random noise and reshape it into a 8 × 8 × 256 tensor through a fully connected layer.

<!-- formula-not-decoded -->

where /epsilon1 is a pre-fixed scaling factor and cli p (.) 1 -1 performs clipping in the range [-1 , 1 ] and I ′ gs is reconstructed image from the discriminator loss.

## C. Loss Functions

Our discriminator computes the loss of the two vectors from j th layer as

<!-- formula-not-decoded -->

where ' K ' represents the number of images in the given class. We back propagate the gradients from the loss to update Igs . Subsequently, I ′ g is taken out to further get the generator loss as

<!-- formula-not-decoded -->

## D. Generator Architecture

The Generator starts with a noise vector n ∈ R 100 . It constructs a 8 × 8 × 256 tensor from this vector in its first layer. Using transposed convolutions, the input is progressively processed such that its base grows while its depth decreases until we reach the final layer with the shape of the image we

- We then use transposed convolution, to transform the data into 8 × 8 × 128 tensor. Note that here the width and the height dimensions remain unchanged, this is achieved by setting the stride parameter in Conv2DTranspose to 1.
- Batch normalization and the Leaky ReLU activation function is applied.
- We repeat the process for all layers as shown in Fig. 3 until the last layer where we use transposed convolution, transforming the 149 × 149 × 8 tensor into the output image size, 299 × 299 × 3.
- The tanh activation function is applied in the last layer.

## E. Discriminator Architecture

In our experiments, we employ Inception-V3 as discriminator with its classification layer chopped off and making ' avg\_pool ' layer as the output layer. The feature vector from this layer serve as the prediction vector and loss is computed over the prediction vectors for target and source images. We freeze the discriminator weights during the generator training. The gradients from the discriminator are back propagated to update the input image. Subsequently, updated generator output is taken out to compute generator loss and generator weights are updated.

## F. Implementation Details

We use ADAM optimizer [66] to minimize our generator and discriminator losses. We set the learning rate to 1 × 10 -4 and train the generator for 300 epochs. All our experiments are performed on NVIDIA TITAN RTX GPU. For each class experiments, we train the generator on train set and validate it by using all the images of the source class in the validation set of 5000 images. Details of the dataset is provided below. We perform testing of our algorithm under gray-box settings where the attack is launched on the captioning framework by manipulating the visual input only. To that end, the baseline is achieved by adopting a vanilla CNN and LSTM/Transformer

Fig. 3. Generator architecture to generate image agnostic perturbations. The generator inputs a uniformly distributed noise vector and outputs a perturbation, which is scaled to satisfy a norm constraint. The perturbation, when added to benign image of source class, is able to fool the target network.

<!-- image -->

combination. We give the architectural details of Transformer model employed in the captioning framework under attack. The model dimension used is d = 512 and the hidden size of feed-forward network layers used is 2048. We set the number of heads H = 4. We use the Adam [66] optimizer with dynamic learning rate. We set β 1 = 0 . 90, β 2 = 0 . 98, and smoothing parameter γ = 0 . 7. For model regularisation, dropout [67] of 0 . 1 is used at the output of each sub-layer before its addition and normalisation, both in encoder and decoder stacks. We employ TensorFlow framework for the development with a NVIDIA Titan RTX GPU.

## IV. EXPERIMENTS AND RESULTS

We discuss the attack performance of our method on popular captioning frameworks i . e ., Show-and-Tell [9], Show-Attendand-Tell [10], and CNN + Transformer architecture. We also perform experiments to explore the internal mechanism of the captioning framework for better understanding of captioning models.

## A. Dataset and Metrics

We evaluate our technique on the benchmark dataset for image captioning i . e ., Microsoft COCO 2014 (MS COCO) [15]. We split the images into 113287, 5000 and 5000 for training, validation and test set following [41]. For training purposes, we further split the images based on their classes and availability of their sufficient number of examples in the training set for generator training. We employ the popular BLEU-1, BLEU-2, BLEU-3, BLEU-4, CIDEr, METEOR, ROUGE and SPICE metrics to evaluate the predicted captions for the targeted adversarial attacks.

## B. Gray-Box Attack

We use gray box setup in our experiments where we do not have any details of the language model of the captioning framework. We perform experiments with known CNN i . e ., feature extractor but no information regarding model's augmentation techniques e . g ., attention or semantic attributes. This is in sharp contrast to the existing methods that take advantage of the target model's objective function to optimize the perturbations [11], [12], [13].

1) Targeted Caption Results: We evaluate our attack on the popular state-of-the-art image captioning models i . e ., Show and Tell [9], and Show-Attend-and-Tell [10] where the latter additionally employs attention mechanism in its framework. To evaluate the attack, we use the MS COCO dataset [15] which is used by the aforementioned and vast majority of other existing methods. To the best of our knowledge, ours is the first and only method that performs gray-box attack on image captioning. Hence, the reported results do not include comparisons to existing methods as there are none in this direction. All existing methods use the language model information and devise their attack strategy based on the adversary's objective functions. In contrast, we manipulate the image caption by an attack completely based on the visual model of the captioning framework.

To evaluate the attack, first we select all the images from the source class and randomly select one image from the target class. Unlike other methods which use the target image's caption, we directly use the target image itself for perturbation generation, and fool the framework to generate a caption for the source image similar to that of the target image. For the generated adversarial captions, we evaluate the attack success rate by measuring all the predictions of the class dataset that match the target captions. Unlike image classification where the image label is fixed, the correct or relevant caption for an image has unlimited space. Multiple captions for an image may be altogether different yet correct. Therefore, we believe that exact match is an inappropriate criterion as it treats semantically correct captions as incorrect. We resolve this issue by employing METEOR score as the metric for match between the two predictions. METEOR has proven to be a robust metric which not only caters for all possible synonyms of the words but is found to be highly correlated with human judgments in settings with low number of reference [68]. As described below, we devise two metrics for caption matching.

1. Exact-Match: The two predictions i . e ., of source image and target image are identical.
2. METEOR Score &gt; τ : The metric measures whether the METEOR score between the captions exceeds beyond a threshold. Inspired by evaluation metrics in dense image/video captioning [17], [26] we use METEOR score thresholds of 0 . 15 , 0 . 20 , 0 . 25.

TABLE II

RESULTS OF ADVERSARIAL ATTACKS ON THE SHOW-AND-TELL [9] MODEL WITH /epsilon1 = [0.05, 0.1, 0.2, 0.3]. τ INDICATES THRESHOLD FOR METEOR METRIC SCORE FOR SIMILARITY COMPARISON BETWEEN PREDICTED AND TARGETED CAPTION. FR DENOTES FOOLING RATE THAT SHOWS THE %AGE OF EXAMPLES SUCCESSFULLY ATTACKED. AVG. || δ || 2 INDICATES THE AVERAGE /lscript 2 -NORM OF THE PERTURBATIONS, COMPUTED OVER ALL THE SUCCESSFUL EXAMPLES

## TABLE III

RESULTS OF ADVERSARIAL ATTACKS ON THE SHOW-ATTEND-AND-TELL [10] MODEL WITH /epsilon1 = [0.05, 0.1, 0.2, 0.3]. τ INDICATES THRESHOLD FOR METEORMETRIC SCORE FOR SIMILARITY COMPARISON BETWEEN PREDICTED AND TARGETED CAPTION. FR DENOTES FOOLING RATE THAT SHOWS THE %AGE OF EXAMPLES SUCCESSFULLY ATTACKED. AVG. || δ || 2 INDICATES THE AVERAGE /lscript 2 -NORM OF THE PERTURBATIONS, COMPUTED OVER ALL THE SUCCESSFUL EXAMPLES

Attack results on Show and Tell Model [9] are shown in Table II. We see that for the exact match the fooling rate varies from 31 . 9% to 64 . 1% for different /epsilon1 values. Considering the gray-box constraint with no information of the language model, these fooling rates are significant. As the exact match is a highly constrained metric for captions comparison, we see that the fooling rates with our derived METEOR metric (which is also more intuitive) are even higher ranging from 71 . 3% to 90 . 1% for different /epsilon1 values. It is emphasized that we include the large /epsilon1 values in our analysis for the sake of comprehensiveness. Our technique shows acceptable FR for /epsilon1 = 0 . 05. The FR score monotonously improves with larger values of /epsilon1 , however it comes at the cost of more perceptibility of the perturbations in the image. In the range /epsilon1 = [ 0 . 2 , 0 . 3 ] , the perturbations are already easily detectable by the human vision system. Hence, we do not report results beyond /epsilon1 = 0 . 3.

## TABLE IV

RESULTS OF ADVERSARIAL ATTACKS WITH DIFFERENT /epsilon1 VALUES ON THE CNN+Transformer ARCHITECTURE. WE EVALUATE GENERATED CAPTIONS FOR CLEAN IMAGES (TO SET THE BASELINE) AND PERTURBED IMAGES WITH BLEU-3 (B3), BLEU-4 (B4) AND METEOR (M). FOOLING RATE IS THE %AGE OF SUCCESSFULLY ATTACKED EXAMPLES WITH METEOR SCORE ABOVE THRESHOLD τ WITH THE TARGETED CAPTION

internal mechanism of the two models. The technique [13] back-propagates the gradients from the observed words to the input image, which can be directly done in the case of Show-Attend-and-Tell. However, in the case of Show-andTell, they need to multiply the latent and observed words gradients first and then back-propagate to the input image. This, in turn, results in the poor performance of the attack on a relatively simpler model. However, our method does not suffer from this bottleneck as we do not use the language model objective function. For qualitative examples please see Fig. 4.

Attack results on Transformer are presented in Table IV. We see a significant performance drop from clean images to perturbed images. The %age of images successfully attacked which produced the desired targeted captions above threshold τ = 0 . 15 varies from 69.4% to 77.2%. This fooling rate is significant given the gray-box constraint. Hence, we can safely conclude that the perturbations computed by our technique

Attack results on Show-Attend-and-Tell Model [10] are presented in Table III. We see from the results that attack performance is slightly better as compared to Show-and-Tell. A possible reason is that the model structures of Showand-Tell and Show-Attend-and-Tell are significantly different from each other. Specifically, in Show-and-Tell model, the extracted visual features by the CNN are fed at the starting time step only. However, Show-Attend-and-Tell model feeds the extracted CNN features at every time step and employs attention mechanism in its language model. This means the model heavily relies on the input visual features. Thus, the perturbations added to the visual features result in better attack performance. Note that, this observation is somewhat different than what is reported in literature [13] i . e ., the attack performance significantly worsens on Showand-Tell model i . e ., from 99 . 56% to 44 . 04%. We believe that the observed phenomenon is due to the variance in the

source\_img

<!-- image -->

<!-- image -->

skier in a red jacket

<!-- image -->

perturbation

<!-- image -->

two white and brown dogs running in a park

<!-- image -->

<!-- image -->

adv\_img

(e = 0.05)

close up of a zebra (M=0.44)

source sianin parkina lot img

<!-- image -->

perturbation

adv\_img (e = 0.05) two white and brown

Fig. 4. Qualitative examples of our method on Show-Attend-and-Tell [10], showing successful attacks i . e ., the model generates the captions of target images given the source images (on which the attack is launched). The target images and their captions are shown next to the source image. M denotes the METEOR score between predicted and target caption.

## TABLE V

PERCENTAGE OF PARTIAL SUCCESS i . e ., PRESENCE OF TARGET KEYWORDS, AT DIFFERENT /epsilon1 VALUES ONLY WITHIN THE FAILED ATTACK EXAMPLES. AVERAGE OF || δ || 2 IS COMPUTED OVER ALL EXAMPLES IN EACH CATEGORY

are effective against multiple decoder structures i . e ., LSTM , LSTM + Attention and Transformer .

2) Failed Attacks and Target/Source Keywords: In addition to the complete caption results, as stated above, we investigate the failed attacks to observe whether the output captions include the keywords or not. Keywords are selected as the intersection of the top-3 predictions by the image classifier and the target caption and consider the attack successful if the predicted captions include the target keyword(s). The results are reported in Table V. As evident from the table, almost 96% of the failed examples include at least one keyword in the predicted caption and almost 90% of the examples contain 3 keywords. Moreover, though the predicted captions achieve low score on the automated metric, we see from the examples that the predicted captions are still relevant to target image content and description (see Fig. 5 for qualitative examples). These results show that even failed attempts are still acceptably fooled.

We also investigate the generated captions with the opposite perspective where we observe if the source keywords are successfully eliminated. The results are reported in Table VI for keyword hiding experiments for 9 different classes. The

zebra standing in an enclosed area with fences\_

<!-- image -->

## TABLE VI

RESULTS FOR HIDING SOURCE KEYWORDS FOR 9 DIFFERENT CLASSES. FR DENOTES FOOLING RATE DENOTING THE %AGE OF EXAMPLES FOR WHICH SOURCE KEYWORD WAS NOT PRESENT IN THE PREDICTED CAPTION

## TABLE VII

COMPARISON WITH THE ONLY AVAILABLE METHOD SHOW-AND-FOOL [12] REPORTING MODEL PERFORMANCE BY ATTACKING THE VISUAL ENCODER. THE SCORES OF THE EXISTING METHODS ARE TAKEN DIRECTLY FROM THE ORIGINAL WORK [12]. THE SCORES ARE BASED ON ATTACKS ON CLASSIFICATION LAYER AS OPPOSED INTERNAL LAYER OF THE VISUAL ENCODER IN OUR METHOD. BOTH ATTACKS EMPLOY SHOW-AND-TELL [9] MODEL. FOOLING RATE (FR) IS THE %AGE OF EXAMPLES SUCCESSFULLY ATTACKED

visibility count is the number of times the selected keyword appears in the predicted captions of the respective class images. It can be seen that we are able to hide selected keywords in the predicted captions with a high success rate for 8 of 9 classes. The 'dog' class has a low success rate of 29%. This relates to ImageNet dataset on which the visual encoder under attack is trained. ImageNet organizes labels in a semantic hierarchy. The 8 classes that have high fooling rate, are at the lowest hierarchy level in ImageNet. However, 'dog' label is higher in the hierarchy, with 147 sub-categories of dogs. The higher level of semantics causes difficulty in fooling. e . g ., French Bulldog can be easily confused with Boston Terrier, but not with a cat.

## C. Comparison to Visual-Only Model Attack

Since our technique attacks the visual model (CNN part) of an image captioning framework, we compare it with the only known method Show and Fool [12] that reports results of attacks on CNN-only, employing the popular I-FGSM [48] and C&amp;W [64] attacks. Table VII shows the comparative results. Show-and-Fool employs Tensorflow implementation of the Show-and-Tell 1 model with Inception-v3 as the CNN. Moreover, it carefully selects 800 images in such a way that it

1 https://github.com/huanzhang12/ImageCaptioningAttack

## TABLE VIII

COMPARISONS OF ADVERSARIAL ATTACKS WITH /epsilon1 = [0.05, 0.1, 0.2, 0.25] ON TWO VANILLA IMAGE CAPTIONING FRAMEWORKS WITH HIDDEN STATE-SIZE (SS) OF 512 (LEFT) AND 2048 (RIGHT) ON VALIDATION SET OF MS COCO DATASET [15]. B-[1-4], M, C, R, AND S REPRESENT EVALUATION METRICS BLEU-[1-4], METEOR, CIDER, ROUGE AND SPICE, RESPECTIVELY

has at least one word common with Show-and-Tell vocabulary with 100% classification accuracy on Inception-v3. In contrast, we do not set any of these constraints. For a fair comparison, we adopt the same CNN model i . e ., Inception-v3 in our implementation and experimental hyperparameter values such as /epsilon1 . 2 The same CNN allows us to process the images of the same sizes. Despite that Show-and-Fool sets very weak criterion of success, we see that our method outperforms it with a significant margin even with the exact match score. We note that, in Table VII, we do not compare with 'Mimic and Fool' (MaF) [62] because our method is not directly comparable to that approach due to the major differences in the technique and the ultimate fooling objective. However, here we do provide a loose performance comparison with a more relevant variant of MaF, i.e., OIMO. As compared to the OMIO's success rate of 56 . 9% on the metric 'Exact Match', for the Show-and-Tell model, our success rate varies between 31 . 9% to 64 . 1% for different /epsilon1 . Similarly, for the Show-Attend-and-Tell, we report a success rate that varies between 39 . 3% to 66 . 7% in comparison to 50 . 3% success rate of OIMO. Note that, OIMO does not provide the /epsilon1 value. Additionally, OIMO is reported to require about 7 . 61 to 36 . 5 seconds to compute a perturbation, whereas our method only performs a single forward pass for this purpose, which can be accomplished in milliseconds.

The results confirm that attacking the image captioning framework is inherently more challenging as it requires more careful designing of the adversarial examples. As seen from the results, attacking the image class label, as done by the other methods, does not perform well in image captioning. However, devising the attack based on the internal layers of the classifier (our method) results in much better performance. It is emphasized that in Table VII, the || δ || 2 values are a byproduct, and not a controllable parameter. Lower values of || δ || 2 is more desirable, as they signify the possibility of lower perceptibility of the perturbations.

## D. Internal Layer Size Effect on Attack Success

In this section, we investigate the effect of the number of LSTM network units on the attack performance. To explore this, we design two vanilla image captioning frameworks without any sophistication such as attention or semantic

2 Note that, C&amp;W uses different hyperparameters, which are not covered in this article. Interested readers are referred to [12] for the used hyperparameter settings of the existing works in Table VII.

<!-- image -->

<!-- image -->

<!-- image -->

source \_img tennis court.

<!-- image -->

three teddy bears giving each other a hug.

<!-- image -->

people walk down a busy city street, with traffic light.

<!-- image -->

adv (e = 0.05) vith hlank img

<!-- image -->

perturbation

source\_img

<!-- image -->

perturbation

adv\_img (€ 0.05)

Fig. 5. Examples of not (fully) successful attacks. The METEOR (M) score of predicted captions fall under the minimum threshold of τ = 0.15, and hence considered unsuccessful. However, the predicted captions remain relevant to the target image.

attributes. We keep all the parameters and training settings similar for both the models and select two hidden layer sizes of the LSTM i . e ., 512 and 2048. Moreover, we perform four experiments on each model using /epsilon1 = { 0 . 05 , 0 . 1 , 0 . 2 , 0 . 25 } . The predicted captions for the whole validation dataset are then evaluated using the popular automated evaluation metrics i . e ., BLEU-[1-4], METEOR, CIDEr, ROUGE and SPICE. The results of this experiment are reported in Table VIII. For upper bounds of the model, we first compute the metric scores using the benign image set as shown in the first row of the Table VIII. We then run the model with adversarial images perturbed with various /epsilon1 values and compute the metric scores for all predictions. Interestingly, the model with hidden state size of 512 performs slightly better on all runs. However, we see that the performance of both models degrade with increase in the /epsilon1 value. The trend is similar in both variants. We analyse another aspect from the experiment regarding the behaviour of the evaluation metrics. We see that B-1, which refers to uni-grams , is least effected by all four attacks. The same effect is corroborated by our keyword experiments where we observe that even in the failed attacks, almost 94% of the captions contain the target (incorrect) keywords.

three teddy bears giving each other hug.

<!-- image -->

a zebra standing in an enclosed area with fences

<!-- image -->

2

<!-- image -->

two white and brown dogs running in a park

2

<!-- image -->

baseball player swinging a bat at ball

<!-- image -->

perturbation

<!-- image -->

perturbation

<!-- image -->

perturbation

<!-- image -->

<!-- image -->

benign\_img

<!-- image -->

benign\_img

<!-- image -->

benign img

<!-- image -->

<!-- image -->

adv\_img (e = 0.05)

<!-- image -->

adv (e = 0.1) img

<!-- image -->

<!-- image -->

benign\_img

adv\_img (e = 0.05)

<!-- image -->

benign\_img

<!-- image -->

<!-- image -->

adv\_img (€ = 0.1)

<!-- image -->

benign\_img

<!-- image -->

adv\_img (€ 0.05)

<!-- image -->

benign\_img

<!-- image -->

<!-- image -->

benign\_img

<!-- image -->

adv\_img (€ = 0.05)

<!-- image -->

adv\_img (e = 0.05)

benign\_img

<!-- image -->

adv\_img (€ 0.05)

perturbation

<!-- image -->

benign\_img

adv\_img (e = 0.05)

benign img

adv\_img (e = 0.05)

benign\_img

adv\_img (e = 0.05)

Fig. 6. Further qualitative results as generated by our technique. M denotes the METEOR score between predicted caption and target caption. Text in green shows the model prediction for benign image. Text in red denotes the examples categorised as failed attack examples.

From Table VIII, we see that both the models show similar trend against the adversarial attack. Thus, we can conclude that the internal state size does not play a major role as a defense against the adversarial attack. The slight difference in both model's performance is inherent due to the state size mismatch, as evident from the results in the first row computed on benign images.

## E. Additional Qualitative Results

In this section, we present further qualitative results of adversarial attacks as crafted by our technique as shown in Fig. 6. The captions in red color denotes the failed category examples. As we can see that though the failed examples could not achieve desired Meteor score, however, the generated captions are still relevant to the target image, while the adversarial noises are invisible to human perception.

## V. CONCLUSION

We studied the adversarial attack on multi-model image captioning framework and proposed an algorithm to generate adversarial examples for that. The algorithm performs a gray-box attack without requiring language module information. Our attack is a first-of-its-kind method that controls the predicted captions by attacking only on the visual encoder of the captioning framework. We demonstrated that our method can generate adversarial examples against any state-of-the-art model with a high attack success rate. We also showed that attack on the classification layer of the visual module results in poor success rate in image captioning, as compared to attacking the internal layer of the feature extractor. Moreover, we observed that the internal state size of the recurrent network does not play any major role in robustification of the model against the adversarial attacks. To the best of our knowledge, ours is the first work on crafting adversarial examples under gray-box setting for the image captioning systems.

## REFERENCES

- [1] N. Akhtar and A. Mian, 'Threat of adversarial attacks on deep learning in computer vision: A survey,' IEEE Access , vol. 6, pp. 14410-14430, 2018.
- [2] C. Szegedy et al., 'Going deeper with convolutions,' in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. , Jun. 2015, pp. 1-9.
- [3] N. Papernot, P. McDaniel, and I. Goodfellow, 'Transferability in machine learning: From phenomena to black-box attacks using adversarial samples,' 2016, arXiv:1605.07277 .
- [4] Y. Liu, X. Chen, C. Liu, and D. Song, 'Delving into transferable adversarial examples and black-box attacks,' 2016, arXiv:1611.02770 .
- [5] I. J. Goodfellow, J. Shlens, and C. Szegedy, 'Explaining and harnessing adversarial examples,' 2014, arXiv:1412.6572 .
- [6] J. Lu, C. Xiong, D. Parikh, and R. Socher, 'Knowing when to look: Adaptive attention via a visual sentinel for image captioning,' in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR) , Jul. 2017, pp. 375-383.
- [7] J. Lu, H. Sibai, E. Fabry, and D. Forsyth, 'Standard detectors aren't (currently) fooled by physical adversarial stop signs,' 2017, arXiv:1710.03337 .
- [8] J. Lu, H. Sibai, E. Fabry, and D. Forsyth, 'NO need to worry about adversarial examples in object detection in autonomous vehicles,' 2017, arXiv:1707.03501 .
- [9] O. Vinyals, A. Toshev, S. Bengio, and D. Erhan, 'Show and tell: A neural image caption generator,' in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR) , Jun. 2015, pp. 3156-3164.
- [10] K. Xu et al., 'Show, attend and tell: Neural image caption generation with visual attention,' in Proc. ICML , 2015, pp. 2048-2057.
- [11] X. Xu, X. Chen, C. Liu, A. Rohrbach, T. Darrell, and D. Song, 'Fooling vision and language models despite localization and attention mechanism,' in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. , Jun. 2018, pp. 4951-4961.
- [12] H. Chen, H. Zhang, P.-Y. Chen, J. Yi, and C.-J. Hsieh, 'Attacking visual language grounding with adversarial examples: A case study on neural image captioning,' in Proc. 56th Annu. Meeting Assoc. Comput. Linguistics , 2018, pp. 2587-2597.
- [13] Y. Xu et al., 'Exact adversarial attack to image captioning via structured output learning with latent variables,' in Proc. IEEE CVPR , 2019, pp. 4135-4144.
- [14] Y. LeCun, Y. Bengio, and G. Hinton, 'Deep learning,' Nature , vol. 521, no. 7553, pp. 436-444, 2015.
- [15] T.-Y. Lin et al., 'Microsoft COCO: Common objects in context,' in Proc. ECCV , 2014, pp. 740-755.
- [16] J. Xu, T. Mei, T. Yao, and Y . Rui, 'MSR-VTT: A large video description dataset for bridging video and language,' in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR) , Jun. 2016, pp. 5288-5296.
- [17] R. Krishna, K. Hata, F. Ren, L. Fei-Fei, and J. C. Niebles, 'Densecaptioning events in videos,' in Proc. IEEE Int. Conf. Comput. Vis. (ICCV) , Oct. 2017, pp. 706-715.
- [18] R. Krishna et al., 'Visual genome: Connecting language and vision using crowdsourced dense image annotations,' Int. J. Comput. Vis. , vol. 123, no. 1, pp. 32-73, 2017.
- [19] B. Pan et al., 'Spatio-temporal graph for video captioning with knowledge distillation,' in Proc. IEEE CVPR , 2020, pp. 10870-10879.
- [20] Y. Feng, L. Ma, W. Liu, and J. Luo, 'Unsupervised image captioning,' in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR) , Jun. 2019, pp. 4125-4134.
- [21] X. Yang, K. Tang, H. Zhang, and J. Cai, 'Auto-encoding scene graphs for image captioning,' in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR) , Jun. 2019, pp. 10685-10694.
- [22] J. Zhang and Y. Peng, 'Video captioning with object-aware spatiotemporal correlation and aggregation,' IEEE Trans. Image Process. , vol. 29, pp. 6209-6222, 2020.
- [23] N. Aafaq, N. Akhtar, W. Liu, S. Z. Gilani, and A. Mian, 'Spatio-temporal dynamics and semantic attribute enriched visual encoding for video captioning,' in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR) , Jun. 2019, pp. 12487-12496.
- [24] S. Liu, Z. Ren, and J. Yuan, 'SibNet: Sibling convolutional encoder for video captioning,' IEEE Trans. Pattern Anal. Mach. Intell. , vol. 43, no. 9, pp. 3259-3272, Sep. 2021.
- [25] J. S. Park, T. Darrell, and A. Rohrbach, 'Identity-aware multi-sentence video description,' in Proc. ECCV , 2020, pp. 360-378.
- [26] J. Johnson, A. Karpathy, and L. Fei-Fei, 'DenseCap: Fully convolutional localization networks for dense captioning,' in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR) , Jun. 2016, pp. 4565-4574.
- [27] K. Cho et al., 'Learning phrase representations using RNN encoderdecoder for statistical machine translation,' in Proc. EMNLP , 2014, pp. 1724-1734.
- [28] S. Hochreiter and J. Schmidhuber, 'Long short-term memory,' Neural Comput. , vol. 9, no. 8, pp. 1735-1780, 1997.
- [29] A. Vaswani et al., 'Attention is all you need,' in Proc. Adv. Neural IPS , 2017, pp. 5998-6008.
- [30] X. Wang, W. Chen, J. Wu, Y.-F. Wang, and W. Y. Wang, 'Video captioning via hierarchical reinforcement learning,' in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. , Jun. 2018, pp. 4213-4222.
- [31] Q. Zheng, C. Wang, and D. Tao, 'Syntax-aware action targeting for video captioning,' in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR) , Jun. 2020, pp. 13096-13105.
- [32] Z. Zhang et al., 'Object relational graph with teacherrecommended learning for video captioning,' in Proc. IEEE/CVF CVPR , Jun. 2020, pp. 13278-13288.
- [33] C. Yan et al., 'STAT: Spatial-temporal attention mechanism for video captioning,' IEEE Trans. Multimedia , vol. 22, no. 1, pp. 229-241, Jan. 2020.
- [34] L. Yao et al., 'Describing videos by exploiting temporal structure,' in Proc. IEEE ICCV , Dec. 2015, pp. 4507-4515.
- [35] Z. Gan et al., 'Semantic compositional networks for visual captioning,' in Proc. IEEE CVPR , Jul. 2017, pp. 5630-5639.
- [36] Y. Pan, T. Yao, H. Li, and T. Mei, 'Video captioning with transferred semantic attributes,' in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR) , Jul. 2017, pp. 6504-6512.
- [37] J. Wang, W. Wang, Y. Huang, L. Wang, and T. Tan, 'M3: Multimodal memory modelling for video captioning,' in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. , Jun. 2018, pp. 7512-7520.
- [38] W. Pei, J. Zhang, X. Wang, L. Ke, X. Shen, and Y.-W. Tai, 'Memory-attended recurrent network for video captioning,' in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR) , Jun. 2019, pp. 8347-8356.
- [39] W. Hao, Z. Zhang, and H. Guan, 'Integrating both visual and audio cues for enhanced video caption,' in Proc. AAAI , 2018, pp. 6894-6901.
- [40] J. Xu, T. Yao, Y. Zhang, and T. Mei, 'Learning multimodal attention LSTM networks for video captioning,' in Proc. 25th ACM Int. Conf. Multimedia , Oct. 2017, pp. 537-545.
- [41] A. Karpathy and L. Fei-Fei, 'Deep visual-semantic alignments for generating image descriptions,' in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR) , Jun. 2015, pp. 3128-3137.
- [42] H. Yu, J. Wang, Z. Huang, Y. Yang, and W. Xu, 'Video paragraph captioning using hierarchical recurrent neural networks,' in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR) , Jun. 2016, pp. 4584-4593.
- [43] Y. Xiong, B. Dai, and D. Lin, 'Move forward and tell: A progressive generator of video descriptions,' in Proc. ECCV , 2018, pp. 468-483.
- [44] C. Szegedy et al., 'Intriguing properties of neural networks,' 2013, arXiv:1312.6199 .

- [45] A. Krizhevsky, I. Sutskever, and G. E. Hinton, 'ImageNet classification with deep convolutional neural networks,' in Proc. Adv. Neural IPS , 2012, pp. 84-90.
- [46] R. Girshick, J. Donahue, T. Darrell, and J. Malik, 'Rich feature hierarchies for accurate object detection and semantic segmentation,' in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. , Jun. 2014, pp. 580-587.
- [47] J. Long, E. Shelhamer, and T. Darrell, 'Fully convolutional networks for semantic segmentation,' in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR) , Jun. 2015, pp. 3431-3440.
- [48] A. Kurakin, I. Goodfellow, and S. Bengio, 'Adversarial machine learning at scale,' in Proc. ICLR , 2017.
- [49] N. Carlini and D. Wagner, 'Towards evaluating the robustness of neural networks,' in Proc. IEEE Symp. Secur. Privacy (SP) , May 2017, pp. 39-57.
- [50] S.-M. Moosavi-Dezfooli, A. Fawzi, and P. Frossard, 'DeepFool: A simple and accurate method to fool deep neural networks,' in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR) , Jun. 2016, pp. 2574-2582.
- [51] N. Inkawhich, W. Wen, H. H. Li, and Y. Chen, 'Feature space perturbations yield more transferable adversarial examples,' in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR) , Jun. 2019, pp. 7066-7074.
- [52] Q. Huang, I. Katsman, Z. Gu, H. He, S. Belongie, and S.-N. Lim, 'Enhancing adversarial example transferability with an intermediate level attack,' in Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV) , Oct. 2019, pp. 4733-4742.
- [53] Q. Xu, G. Tao, S. Cheng, and X. Zhang, 'Towards feature space adversarial attack,' 2020, arXiv:2004.12385 .
- [54] C. Xie, J. Wang, Z. Zhang, Y. Zhou, L. Xie, and A. Yuille, 'Adversarial examples for semantic segmentation and object detection,' in Proc. IEEE Int. Conf. Comput. Vis. (ICCV) , Oct. 2017, pp. 1369-1378.
- [55] D. Song et al., 'Physical adversarial examples for object detectors,' in Proc. 12th Workshop Offensive Technol. (WOOT) , 2018.
- [56] A. Arnab, O. Miksik, and P. H. Torr, 'On the robustness of semantic segmentation models to adversarial attacks,' in Proc. IEEE CVPR , Jun. 2018, pp. 888-897.
- [57] N. Papernot, P. McDaniel, A. Swami, and R. Harang, 'Crafting adversarial input sequences for recurrent neural networks,' in Proc. IEEE Mil. Commun. Conf. , Nov. 2016, pp. 49-54.
- [58] R. Jia and P. Liang, 'Adversarial examples for evaluating reading comprehension systems,' 2017, arXiv:1707.07328 .
- [59] Y.-C. Lin, Z.-W. Hong, Y.-H. Liao, M.-L. Shih, M.-Y. Liu, and M. Sun, 'Tactics of adversarial attack on deep reinforcement learning agents,' 2017, arXiv:1703.06748 .

[60] J. Kos and D. Song, 'Delving into adversarial attacks on deep policies,' 2017, arXiv:1705.06452 .

- [61] S. Huang, N. Papernot, I. Goodfellow, Y. Duan, and P. Abbeel, 'Adversarial attacks on neural network policies,' 2017, arXiv:1702. 02284 .
- [62] A. Chaturvedi and U. Garain, 'Mimic and fool: A task-agnostic adversarial attack,' IEEE Trans. Neural Netw. Learn. Syst. , vol. 32, no. 4, pp. 1801-1808, Apr. 2021.
- [63] A. Mahendran and A. Vedaldi, 'Understanding deep image representations by inverting them,' in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR) , Jun. 2015, pp. 5188-5196.

[64] N. Carlini and D. Wagner, 'Adversarial examples are not easily detected: Bypassing ten detection methods,' in Proc. 10th ACM Workshop Artif. Intell. Secur. , Nov. 2017, pp. 3-14.

- [65] A. Madry, A. Makelov, L. Schmidt, D. Tsipras, and A. Vladu, 'Towards deep learning models resistant to adversarial attacks,' 2017, arXiv:1706.06083 .

[66] D. P. Kingma and J. Ba, 'Adam: A method for stochastic optimization,' in Proc. ICLR , 2015.

- [67] N. Srivastava, G. Hinton, A. Krizhevsky, I. Sutskever, and R. Salakhutdinov, 'Dropout: A simple way to prevent neural networks from overfitting,' J. Mach. Learn. Res. , vol. 15, no. 1, pp. 1929-1958, Jan. 2014.
- [68] R. Vedantam, C. L. Zitnick, and D. Parikh, 'CIDEr: Consensus-based image description evaluation,' in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR) , Jun. 2015, pp. 4566-4575.

<!-- image -->

Nayyer Aafaq received the B.E. degree (Hons.) in avionics from the College of Aeronautical Engineering (CAE), National University of Sciences and Technology (NUST), Pakistan, in 2007, the M.S. degree (Hons.) in systems engineering from the Queensland University of Technology (QUT), Australia, in 2012, and the Ph.D. degree from the School of Computer Science and Software Engineering (CSSE), The University of Western Australia (UWA). His Ph.D. thesis won Dean's List for Outstanding Thesis Award. He is currently working as an Assistant Professor with the NUST. His research in computer vision and pattern recognition has been published in prestigious venues of the field, including IEEE CVPR, IEEE TRANSACTIONS ON MULTIMEDIA, IEEE TRANSACTIONS ON ARTIFICIAL INTELLIGENCE, and ACM Computing Surveys (ACM CSUR). His current research interests include deep learning, video analysis and intersection of natural language processing (NLP), computer vision (CV), and artificial intelligence. He was a recipient of SIRF Scholarship with UWA.

<!-- image -->

Naveed Akhtar (Member, IEEE) received the master's degree from Hochschule Bonn-Rhein-Sieg, Germany, and the Ph.D. degree in computer science from The University of Western Australia (UWA). He is currently a Senior Research Fellow with UWA. His research is regularly published in the prestigious sources of computer vision, including IEEE TRANSACTIONS PATTERN ANALYSIS AND MACHINE INTELLIGENCE, IEEE Conferences on Computer Vision and Pattern Recognition (CVPR), and European Conference on Computer Vision

(ECCV). His research interests include adversarial machine learning, robotics, explainable artificial intelligence, and hyperspectral image analysis. He was a recipient of the prestigious Fellowship by the Australian Office of National Intelligence. He is a Finalist of the Western Australia's Early Career Scientist of the Year 2021 and Universal Scientific Education and Research Network top ten young scientist in Formal Sciences for 2021. He also serves/served as an Area Chair for CVPR 2022, ECCV 2022, and WACV 2022. He serves as an Associate Editor for IEEE TRANSACTIONS NEURAL NETWORKS AND LEARNING SYSTEMS and IEEE ACCESS, and a Guest Editor of Neural Computing and Applications and Remote Sensing journals . He is an ACM Distinguished Speaker.

<!-- image -->

Wei Liu received the Ph.D. degree from the University of Newcastle, Australia, in 2003. She is currently working with the Department of Computer Science and Software Engineering, The University of Western Australia, and a Co-Lead of the Faculty's Big Data Research Group. Her research impact in the field of knowledge discovery from natural language text data is evident by a series of highly cited papers, and the reputable top data mining and knowledge management journals and conferences that she has been published in. These include for example, ACM Computer Surveys , Journal of Data Mining and Knowledge Discovery , Knowledge and Information Systems , International Conference on Data Engineering (ICDE), and ACM International Conference on Information and Knowledge Management (CIKM). She has won three Australian Research Council Grants and several industry grants. Her current research interests include deep learning methods for knowledge graph construction from natural language text, sequential data mining, and text mining.

<!-- image -->

Mubarak Shah (Life Fellow, IEEE) is currently the Trustee Chair Professor of computer science and the Founding Director of the Center for Research in Computer Vision, University of Central Florida (UCF). His research interests include video surveillance, visual tracking, human activity recognition, visual analysis of crowded scenes, video registration, and UAV video analysis. He is a fellow of the AAAS, IAPR, and SPIE. He received the IEEE Outstanding Engineering Educator Award in 1997. In 2006, he was awarded a Pegasus Professor

Award, the highest award at UCF. He received the Harris Corporations Engineering Achievement Award in 1999, the TOKTEN Awards from UNDP in 1995, 1997, and 2000, the Teaching Incentive Program Award in 1995 and 2003, the Research Incentive Award in 2003 and 2009, the Millionaires Club Awards in 2005 and 2006, the University Distinguished Researcher Award in 2007, and the Honorable mention for the ICCV 2005 Where Am I? Challenge Problem, and was nominated for the Best Paper Award at the ACM Multimedia Conference in 2005. He was the Program Co-Chair of CVPR 2008. He is an Editor of an International Book Series on Video Computing. He was the Editor-in-Chief of Machine Vision and Applications journal, an Associate Editor of ACM Computing Surveys journal, and an Associate Editor of IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE. He was a Guest Editor of the Special Issue of International Journal of Computer Vision on Video Computing . He is an ACM Distinguished Speaker. He was an IEEE Distinguished Visitor Speaker from 1997 to 2000.

<!-- image -->

Ajmal Mian (Senior Member, IEEE) is currently a Professor of computer science with The University of Western Australia. His research interests include computer vision, deep learning, video analysis, human action recognition, 3-D point cloud analysis, and facial recognition. He is a fellow of the International Association for Pattern Recognition. He was a recipient of three prestigious national-level fellowships from the Australian Research Council (ARC), including the Future Fellowship Award. He received the West Australian Early Career Sci- entist of the Year Award 2012, the HBF Mid-Career Scientist of the Year Award 2022, and several other awards, including the Excellence in Research Supervision Award, the EH Thompson Award, the ASPIRE Professional Development Award, the Vice-Chancellors Mid-Career Research Award, the Outstanding Young Investigator Award, and the Australasian Distinguished Doctoral Dissertation Award. He has secured research funding from the ARC, the National Health and Medical Research Council of Australia, the U.S. Department of Defense DARPA, and the Australian Department of Defense. He was a General Chair of the Asian Conference on Computer Vision in 2018 and the International Conference on Digital Image Computing Techniques and Applications in 2019. He is a Senior Editor of IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS and an Associate Editor of IEEE TRANSACTIONS ON IMAGE PROCESSING and Pattern Recognition .