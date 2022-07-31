## **Introduction**

Most of the sales product images uploaded online stores or SNS have background settings that highlight the features of the products. However, it is not only time-consuming but laborous to set studio, prepare background props and take photos of every product.


![](https://user-images.githubusercontent.com/36873797/182028144-e8f56208-3e32-4753-8a92-a0c3f78b8289.png)*Carefully chosen background assets are necessary in that they highlight unique features of the sales products.*

Fortunately AI technology has developed enough to relieve the burden of it. Recently OpenAI's CLIP model has shown remarkable performance in image captioning task. If AI model can fully understand and describe the given image into natural language, it may be possible to use it in recommendation as well. <br>

![human manager](https://user-images.githubusercontent.com/36873797/182028433-6af04b54-5afa-4712-8045-c6dd79a4e292.png)*From preparing for props and studio settings to choosing selling photos, it takes considerable time and cost for a human manager to complete the background images.*


![AI model](https://user-images.githubusercontent.com/36873797/182028635-44dddc89-cd99-4a69-9482-2799e1709bd6.png)
*Our goal is to easily handle the laborous tasks under the guidance of reliable AI model.*

  
Leveraging its zero-shot learning ability, we(with my colleagues Gwan Hyeong Koo and Kyu Eol Park) implemented text-text based image recommendation system. Our source codes are based on Google’s Socratic Models([https://socraticmodels.github.io](https://socraticmodels.github.io/)) which can be considered combination of CLIP and GPT-3 model. The followings are detailed explanation of method.


## Step 1. Feature Extraction

First, find out the features of sales products. Is it food, or cosmetics? Is it one of luxury brands or casual ones? Depending on their various features, studio settings need to be adjusted deliberately. The features are extracted in form of text, and categories of the features can be modified by. Here we limited the categories to 1) object type 2) color 3) size 4) mood.

## **Step 2. Text Generation**

From the extracted features, generate complete sentences with recommendation. We used OpenAI’s completion API, where GPT-3 shows amazing text generation results. But be aware of GPT-3’s fluency: it often creates imaginary objects and descriptions absent in original images to solely complete natural contexts between the words.

![summary](https://user-images.githubusercontent.com/36873797/182028659-8f508fed-284a-4b93-a8dd-ffd2dd91215f.png)


### **Step 3. Background Asset**

Here we assumed that background asset(collection of background images) is given in advance. An ideal goal is to generate novel, realistic background images for each selling item, but currently pretraining and implementing image generation models(e.g. OpenAI’s DALL·E, Google’s Imagen) is beyond our capability. Yet simpler and possibly faster alternative is to search through the given background assets. The main task is now narrowed down to finding the most relevant images to the input product features.

### Step 4. Recommendation System

Another problem is to measure relevance between the background asset and a sales product. In other words, can we measure how good an item blends into the background? Instead of directly feeding 2D image data into AI model, we took an additional step of converting image into text caption. 

### **Text-Text Similarity Matching**

The three main prerequisites are 1) our AI model returns image captions that provide sufficient information about the input image, 2) given a pair of captions, semantic similarity between them can be measured and computed 3) If the pair of captions from the two different image(one is a sales product, one is background asset) are similar, it can be assumed that the two images matchewell with each other. In other words, recommendation is based on text-to-text similarity.

## Results

Our demo website link: [http://recommendation.vrin.co.kr:9080/](http://recommendation.vrin.co.kr:9080/)

**However, the demo website is currently closed due to server management cost.** 

If you would like to see our demo or have better idea for improvement, we are always open to your idea. Please email me(sankim3@gmail.com) or post an issue on this github repository, and we are willing to share your idea as soon as possible.

Here are the captured images of our demo website: [http://recommendation.vrin.co.kr:9080/](http://recommendation.vrin.co.kr:9080/)

![web demo 1](https://user-images.githubusercontent.com/36873797/182028673-529a473f-26b2-4e18-96b2-8f070fa6add1.png)

![web demo 2](https://user-images.githubusercontent.com/36873797/182028682-a15da007-cbb8-4449-8565-f581080097ee.png)


