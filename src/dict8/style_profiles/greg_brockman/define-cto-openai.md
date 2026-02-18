It’s been two years since I wrote [#define CTO](https://blog.gregbrockman.com/figuring-out-the-cto-role-at-stripe), in which I documented my quest for a role where I could have scalable impact by writing code. I’ve finally found that role, though not by seeking it — instead, I sought out a problem more important to me than my role within it, brought together the right people, and found that I can best make them effective by writing code.

## Formation [#](https://blog.gregbrockman.com/define-cto-openai#formation_1)

In August 2015, OpenAI was just an idea articulated over a [dinner](https://blog.gregbrockman.com/my-path-to-openai#the-dinner_1) with **Elon Musk**, **Sam Altman**, **Ilya Sutskever**, me, and a handful of others. We’d each come to the dinner with our own ideas, but Elon and Sam had a crisp vision of building safe AI in a project dedicated to benefiting humanity. I wanted to contribute however I could. Sam and I started rallying a team to turn this idea into reality.

We were missing a core ingredient: we needed an AI technical visionary, someone whose intuition and ideas we could follow to the breakthroughs.

[Ilya Sutskever](http://www.cs.toronto.edu/%7Eilya/) was clearly the best person in the world for this. Ilya is best described as an artist who expresses himself through machine learning (and sometimes through paint). [Geoff Hinton](http://www.cs.toronto.edu/%7Ehinton/) once told me that [AlexNet](https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks.pdf), which triggered the deep learning revolution in computer vision, was due to [Alex Krizhevsky](http://www.cs.toronto.edu/%7Ekriz/)’s GPU coding skills and Ilya’s conviction that a deep neural network was bound to win on [ImageNet](http://image-net.org/). (Geoff is proud to have contributed a management trick[1](https://blog.gregbrockman.com/define-cto-openai#fn1).)

I’d always thought I could only co-found a company with someone I’d already known for years. But when Ilya and I grabbed dinner in Mountain View in late August, I knew it was going to work though we’d just met in July. Ilya and I had an extremely high-bandwidth interaction. I didn’t know much about machine learning research, and he didn’t know much about engineering and team building, but we were each impressed with the others’ accomplishments and wanted to learn from each other.

Our ideas enhanced and complemented one another. Ilya thought top researchers would want to work at an AI organization dedicated to making the best outcome for the world, and I’d long thought that combining the resources of private industry with the mission of academia was the way to solve otherwise intractable problems. Without intervention, AI will play out like self-driving cars — a cooperative start followed by a technological race once its potential is proven. But human-level AI will be a transformative technology unlike any other, with unique risks and benefits. Here we saw an opportunity to keep the field cooperative, and to gather many of the best researchers to make a responsible attempt for the most important technological breakthrough in history.

Ilya and I worked together up until launch defining the organization. We talked about strategy (what we would work on), culture (the kind of people we wanted to hire, valuing engineering and research equally), and tactics (hold a daily reading group). We had dinner with Alan Kay, who regaled us with [Xerox PARC](http://www.goodreads.com/book/show/1101290.Dealers_of_Lightning) stories of building the [Alto](https://en.wikipedia.org/wiki/Xerox_Alto) and “living in the future” by using hardware that would cost $1,000 in a decade. Afterwards, Ilya summed up the meal aptly: “I only understood 50% of what he said, but it was all so inspiring.” But that meal helped us validate many of our hypotheses for what would make an impactful organization combining engineering and research.

## Founding team [#](https://blog.gregbrockman.com/define-cto-openai#founding-team_1)

Because Ilya was still at Google, he was unable to help recruit. Between August and November, the job of building the founding team fell to me. I was new to AI, and it wasn’t clear how to find and recruit great researchers. I started by focusing on the [July dinner](https://blog.gregbrockman.com/my-path-to-openai#the-dinner_1) attendees, but wasn’t able to get anyone to join. My next step was to chain through my network, soliciting referrals from each person in turn. It was different from the recruiting I was used to. In startups, the first challenge is always selling the candidate on the mission, but here mission immediately resonated. The challenge was convincing the candidate to believe in this unformed organization.

The dense network of top people in the field helped a lot. I’d been introduced to **Andrej Karpathy** and **Wojciech Zaremba** by a friend, and both were pretty skeptical because I was from outside the field. Yoshua Bengio introduced me to **Durk Kingma**, who was tentatively interested. The tipping point was when a friend of a friend introduced me to **John Schulman** — he immediately knew that this organization, combining the openness and mission of academia with the resources of private industry, was what he was looking for and signed up. His endorsement made Andrej and Wojciech pay attention.

Hiring engineers was easier. **Trevor Blackwell** was a roboticist and YC partner who had been talking to Sam about this crazy idea we were planning. **Vicki Cheung** applied after we launched our sponsoring organization, [YC Research](http://ycr.org/): we hadn’t even announced that we were working on AI, but she was inspired by YC Research’s structure and was excited to work on whatever was needed.

## Solidifying [#](https://blog.gregbrockman.com/define-cto-openai#solidifying_1)

By early November, we had a strong sense of who the founding team would be, but we still needed to get everyone to formally join. At Sam’s suggestion, we invited all of our candidates to an offsite. Everyone clicked in a really visceral way, and the ideas and vision were flowing. (In fact, this offsite is where Andrej suggested the idea that ultimately became [Universe](https://universe.openai.com/).) Our van got stuck in a traffic jam on the way back, but people were enjoying the conversation so much they barely noticed.

_Stroll during the offsite._

[![Image 1: Stroll during the offsite.](https://svbtleusercontent.com/yzuhfxt0alhwrq_small.jpg)](https://svbtleusercontent.com/yzuhfxt0alhwrq.jpg)

We made offers to each of the attendees, and set the offer expiry to December 1st so we could launch at the [NIPS](https://nips.cc/) machine learning conference in early December.

Thus began “closing month”. Sam, Elon, and I chatted with each potential team member. Our priority was making people feel that this was really happening. Every candidate accepted, except one engineer who decided to switch away from AI entirely.

## Spinup [#](https://blog.gregbrockman.com/define-cto-openai#spinup_1)

In the Mythical Man Month, Fred Brooks references a Robert Heinlein story about a project to reach the moon[2](https://blog.gregbrockman.com/define-cto-openai#fn2). The project’s chief engineer is constantly distracted by operational tasks, such as decisions about trucks or telephones, until he takes on a report whose job it is to remove all non-technical tasks from his plate.

This struck me as the right way to run a project to build AI. Technical leadership should call the shots while still doing hands-on technical work. I didn’t know when my engineering skills would be needed, and in the meanwhile I resolved to do whatever was needed to remove all non-research tasks from Ilya’s plate.

On January 4th, the team showed up at our first office (my apartment) to begin work. In the midst of a discussion, John and Ilya turned to write something on the whiteboard, only to realize my apartment had no whiteboards. I quickly got them a whiteboard and any other office supplies they needed.

_Our first office, complete with our first whiteboard._

![Image 2: Our first office](https://lh3.googleusercontent.com/gNw26-Q10Jr4uiWkWbBBZJN4q2ldL6-4cGfPCDGK6I2sx9foLzecPXoSAyQnNGRW1cyk57XSyUU0JVbCt1JigwZqL32Gc495NuKUXv3-2uUTHAET-UGn0aIshTr9SLZGebBfeqJmPkLU62j-Ayawg2JhI2gQk6DDalG8LbrozaXz3ZiDROJpLPOvBHWfFMEamJMrEdo3L5FbOMCjJtl7kjb6cAsCh2qfAB8ZrfiSMcAiThbJUqbVsok4YP4FAGDK5OHrxsA-kUXWB5bSHN-2A2bDNBIuEat_tyWa3c7m_zTiLAtWIEIxkQGzK86nRcjKo3ewptBqW1_DPFN0hx_R9nC3hlHWtnVkSpMfFX-sC5_ihjmfM5Pw_6J4i9X6ECheARrUn2mITCH_MHC8eRPPF8YcmVIhlzq0u2LJX3Ug8f50naVlpOPhfRgJ8ggMp3xVyx1wF1hULy1PufBlDazA_rK-5ZFFyzYcCI0Iy0dcy51RYseEXlS158mRp2VuCsL_sRKZrTJDA3giXE5IXJ0bhP0xQP0dLpIv0mpihPn54i2lsvDyVUkHFAd0zfhOFkeKUk6yrmrvN5YnBhR6mXC8SSHyYQRoZkaMJcl_MtVdRxqcJRGCc6owMKl67Ata3pXmYDU5GKZyWK3uUZVYhZtHysHW6M4h-zzcykPK0pZxgaA=w1440-h1080-no)

For the rest of January, my role was organizing the team, helping figure out who would be working on what, and what we wanted to get done. We talked about what we value in researchers, using our conclusions to design and run an interview process. We had conversations about our vision, how we wanted to work, and what we wanted to get done. Vicki and I procured servers, created Google Apps accounts, and did a bit of maintenance on the Kubernetes cluster that we had spun up in December.

I spent my remaining time reading **Ian Goodfellow**‘s deep learning [textbook](http://www.deeplearningbook.org/). (This doubled as a recruiting strategy, since he was impressed that my pages of comments were more thorough than those from his official reviewers.)

## Gym [#](https://blog.gregbrockman.com/define-cto-openai#gym_1)

Problems in machine learning are more often solved when a new dataset becomes available than when a new algorithm becomes available. Wojciech suggested building a library to standardize [reinforcement learning](http://karpathy.github.io/2016/05/31/rl/) environments (which are effectively dynamic datasets), now called [Gym](https://github.com/openai/gym). The quality of this codebase soon became the high-order bit on our iteration speed. At the end of February, John and I talked about how long it’d take to get to public release. On the current trajectory, he thought it’d probably take until the end of the year.

_A [Fetch](http://fetchrobotics.com/research/) robot we’re training with machine learning. Gym supports controlling [physical robots](https://github.com/openai/rosbridge) as well as simulated ones._

[![Image 3: IMG_3111.JPG](https://svbtleusercontent.com/v7kahsape0vjxw_small.jpg)](https://svbtleusercontent.com/v7kahsape0vjxw.jpg)

Suddenly, engineering had become a bottleneck on research progress. Ilya and I swapped roles — he took on the administrative tasks so I could focus on technical work. After scoping out the work with John, we knew we could have the library built by the end of April.

At Stripe, I’d found a repeatable pattern for creating software systems from nothing: focus single-mindedly on the software, shutting out all distractions and working from wake until sleep, which would inspire others to contribute their best work (importantly, measured by output quality rather than hours). These are the times I feel most alive: coding feels like magic made real, where anything I can imagine and describe becomes possible. This pattern yielded Stripe’s credit card vault (built in my two weeks home for the holidays in 2010), credit card authorization flow (built in three weeks rather than the bank-speed 6-12 months), and [Capture the Flag](https://stripe.com/blog/ctf3-launch) competitions (usually 3 weeks of my work, plus the same in total from others). Tactically, I choose a “soft” and a “hard” launch date spaced out by a week or two; I’ve never hit a soft launch date, but have never missed a hard one.

This work came with an unfamiliar challenge: I wasn’t a domain expert. At first, this caused a lot of friction. I’d build an abstraction to help Wojciech’s workflow, and John would find it hindered his. But pretty soon, I got a feel for which choices would impact the research workflow (such as how people record metrics) and which details the researchers wouldn’t care about (such as how people record videos). After identifying whether a case mattered for research, making the best choice required a certain humility — I would produce five possible alternatives, and John would say that four of them were bad. But the majority of design decisions could be made with domain-agnostic software engineering intuitions.

Fortunately, I did not have to go it alone. About six weeks prior to launch, **Jonas Schneider**, who had worked on CTF 3 with me at Stripe, reached out. Within a few days, we were collaborating on Gym. He was in Germany, and so we ended up with around-the-clock progress on the project with daily handoffs. There’s a real magic to someone where you’ve already established a working dynamic, and our close collaboration wouldn’t have worked if we were starting from scratch.

_Handing out T-shirts at the OpenAI [ICLR](http://www.iclr.cc/doku.php?id=ICLR2016:main&redirect=1) meetup, shortly after Gym launch._

[![Image 4: IMG_1474.JPG](https://svbtleusercontent.com/ebwnsziejle1q_small.jpg)](https://svbtleusercontent.com/ebwnsziejle1q.jpg)

Overall, machine learning systems can be thought of as a machine learning core — usually an advanced algorithm which requires a few chapters from Ian’s book to understand — surrounded by a huge amount of software engineering. The engineering can be shuffling around data, providing wrappers around inputs and outputs, or scheduling distributed code, all of which interface with the core as a black box. A machine learning advance happens when engineering effort plus research effort exceeds some threshold. Each incremental bit of engineering effort (such as decreasing [Universe](https://universe.openai.com/) latencies) makes problems incrementally easier for our models, and has a chance to push the research over the finish line.

## Universe [#](https://blog.gregbrockman.com/define-cto-openai#universe_1)

After the Gym launch in April, Ilya and I worked to scale our organizational processes, defining our team structure and goals with guidance from Sam and Elon during their weekly visits.

_Team working in first actual office. Whiteboard is still present, just not pictured here._

![Image 5: Team working in first actual office](https://lh3.googleusercontent.com/6QBbL1-Osd4J6eJ67rNjhPnF6X3vgldSYdlKpVRgzethb49pMx1PWoBTOBDPOjqTl_1byIQAb5NBROyDQdj2l-TxjHOs5VTp-VxXM-gi0c5VsaywBYIoArKGwSeltmnd_LhM6mmJsUODIBrb8AR0iVOAsDVP-TYvfiXhDVgC7nlaFPkYZwcH2VwofpD_tMRmoRToCJCWOSk06k75vuoLb-BWZpdOOsBwyaPCJS4vdrfgp3cUiPfNeHHocYbXxEnN0YWSgyf4yrKOXbMvd8Ncj3sjBzLr6WntepNNEXs2DU6O6EfKiX5wduzfCipxNK1SNlvFo7WP-zpPi1LHeBpUkjNhN2octftugdhFZKrird-tnNbDcjXosGO2unooQVPfGxYe9Mq-L4w8eoOlfnYWNSxghanemebUwCYbnaqn78bC1vgnQchVNiTJPIk3N_7xg3r6e-3P78TAxNJkuYlnRSw_vEfbX-bRsam0RRYzmSY6EhBy90Y3NvsBXshc2aW2mTYbiehRzr6i6iZuX0DtohlXGBEbxdeyGRF1hoXNnxhFBWOx4-KWp2LKDyfw-ndvHJAF8U7aiW3BUOeN1UZFkQ310VMV0U1Iw6A_8f2h9Ujh5yjuCvE23uFF6WZGUHbrd1w-K4tyDL3sGlHWQghl9UvD2mVWaNLREvNoK2OxIZw=w1546-h404-no)

Our plans required an AI environment with a huge amount of diversity and complexity. Andrej’s suggestion of building an agent to control a web browser seemed like the right idea, but he’d run into friction with [Selenium](http://www.seleniumhq.org/). I started toying with the idea of using VNC to allow an agent to drive an entire desktop from pixels.

But we saw many risks with this approach. For example, DeepMind’s 2013 [Atari paper](https://www.cs.toronto.edu/%7Evmnih/docs/dqn.pdf) took fifty hours to train Pong from pixels, and our environments would be harder than Pong. If even small-scale experiments would take us days, then we’d never make progress. So we set an internal derisking goal of getting an agent to learn Pong in an hour. (Today we have an implementation which solves Pong in ten minutes.)

As with Gym, I focused narrowly on building the VNC system, now called [Universe](https://universe.openai.com/). Unlike Gym, this project wasn’t to support our existing flavor of research, but instead to ask entirely new questions. At this point, each of our teams had leads, who were responsible for looking after their team members, and one of our engineers, **Jie Tang**, had taken the lead on recruiting. So the administrative burden didn’t fall entirely on Ilya. This was fortunate, since it allowed Ilya to build agents for the very first version of this risky project.

_A Universe agent which is randomly sampling from the full action space (i.e. it’s randomly clicking and pushing keys). See the [Universe release post](https://openai.com/blog/universe/#validating-infra) for more well-behaved agents._

Your browser does not support the video tag.

Universe was a long enough project that I needed to split time with running the organization. I found a balance that works for me. When I’m in coding mode, I operate on a block time basis: a single meeting will kill productivity for the entire morning or afternoon. If I have meetings in both the morning and afternoon, I’ll be too drained for productive evening coding. So I started restricting my meetings to early morning or right after lunch, not doing more than three meetings on any given day, and not doing blocks with meetings more than once every other day.

Building Universe was a systems research effort unto itself: while the high-level specification was simple (allow an agent to use a keyboard/mouse/screen), no one had ever tried building a similar system. VNC has long allowed humans to control a remote machine, but there was no solution for programmatically controlling dozens at a time. When we needed to measure the system’s end-to-end latency, **Catherine Olsson** and I built a system to embed timestamps into the image. Sometimes the challenges were non-technical: when research became blocked due to limited training data, within 24 hours **Tom Brown** had spun up a team of contractors to play the games. Or sometimes they were just obscure, as when **Jonathan Gray** noticed that game dynamics could differ between our contractors and AIs due to low CPU on contractors’ laptops. One day I was slogging through restructuring some JSON benchmark specifications, and had a realization: we needed to restructure these because no one had ever tried benchmarking a single agent across thousands of games. At OpenAI, even the slogwork is fundamental.

Over the next few months, **Dario Amodei** and **Rafał Józefowicz** led the research on Universe. They were both night owls, and many nights I’d stay up with them, fixing any issues they ran into. Sometimes I’d wish I was in bed, but each bugfix accelerated the research by a few hours at a time. There’s something extremely validating about your work allowing researchers to ask questions that no human ever has before.

_Universe team meeting in our current office._

![Image 6: Universe team meeting](https://lh3.googleusercontent.com/P2RpgLXDDXyG7tmrXnnqc0l-lkA9tngFWwNtkWnv2vc6CakrLgNZ8cv5C2z3a31aWnhWgzFztIrDGOB09fKzGDEjsmhOQO9bN0CaZjI47oyYOJTeWEdfHVTuVDDEYCaHSKq2UvLPCvdf6HwCLfTPeVBLHDU-JYelB4K8vSfFCS31xn4KFSRaMuuFreQlPz452BVmGe-GY7U0j4wMPklQxkwNOoYhsMheT4-kl8zmgNty5hpLZLwH7Vk_EsHW4qYD3EUTlWQ9vZ59AMmMUQDgyXXAdJYc4KeELYDBFzUGfnLNoHKa1U8SmbuS8qyItbOS66Z0y6bJJnKk9mNKNOBwBzFiopNc7O9NBmeFw-oV94wArfsXqTt7gS3dHzwHjGB6Qea_ac6Y4wdRI7Uu_KLFVjPyPbJUNWoTp3rcqun-J4QniBgY52D0q_NKBIRfu08BT5er2JEP1NM6i4FM_WnOrjXWqXWKc7rhUs3luSOlJoj84Rgftov5Lpv-EgKuXkDBNxM5gCZPb2kKfudAK-y2lDD-pM2UFFK--kXNw3GiSwINTPBdYgpYX57a9F5rM_2yqhQUwMc-NBiFwh3m13UEdXGAI6rrTuxsz33kcDyqYQNYld4WDA1ta8xcfA6JKPsRI_P1ECFbE9iMT47Mt7KSXtYuhq3GWdc4G1XZmFcToPA=w1498-h1123-no)

By launch, the Universe team had grown to about twenty people. It is now a flagship project and a core part of our research strategy (we’ll be ready to share initial results soon). Universe is an example of how engineering is the bottleneck for today’s ML research. It makes me wonder how there were ever days when all I had to do was read Ian’s book.

## What comes next [#](https://blog.gregbrockman.com/define-cto-openai#what-comes-next_1)

We’re now an organization of forty people, and we now need someone optimizing the organization full-time. Since the beginning of OpenAI, we’d been looking for the right first manager to hire. A few months ago, Sam had clued me into a particularly outstanding engineering executor: **Erika Reinhardt**, who had been Director of Product Engineering at Planet Labs, and was now running [voteplz.org](http://voteplz.org/) with him. At Planet Labs, Erika had one of the deepest understandings of the end-to-end satellite imaging system. She works hard, gets things done, is consistently described by former coworkers as one of the smartest people they’ve worked with, and is extremely motivated by mission and impact. So Sam and I launched a plan to recruit her.

_OpenAI team retreat in early October 2016._

[![Image 7: 14608656_10102274815947598_1291726270290750856_o.jpg](https://svbtleusercontent.com/wfds31muayuq_small.jpg)](https://svbtleusercontent.com/wfds31muayuq.jpg)

The most compelling pitch, however, was when she came in to work with us between the election and Universe launch. She found that her leadership skills apply extremely well in this environment, just as I found with my engineering skills. She told me the moment that she was sure she wanted to join was watching [OpenAI’s testimony](http://www.commerce.senate.gov/public/index.cfm/hearings?ID=042DC718-9250-44C0-9BFE-E0371AFAEBAB) at the first Senate hearing on AI — we’re at the beginning of a major technological shift, and getting that right is all that matters.

At Stripe, [Marc Hedlund](https://blog.gregbrockman.com/figuring-out-the-cto-role-at-stripe#hiring-a-vp-engineering_1) and I would often run into issues he’d seen at many previous organizations. He’d like to joke that all companies are the same. There’s remarkable truth to this: if you zoom out, they are all just groups of people organized around a goal. However, each organization has a differentiator that depends on the problem it’s solving.

Most startups create one technology, and then operate and scale it over time. OpenAI is a factory for creating new technologies, which means that we must structure the company to create new things. We have infrastructure and large codebases to maintain, but they serve our need to move quickly, innovate, and find new heights through a combination of software engineering and machine learning research.

OpenAI is an organization where the CTO role is naturally the activity I love most in the world: coding. But even so, people remain my focus: the journey to this point was about a social story, not a technical one. Going forward, this role is only sustainable because I’m part of a fantastic team who is willing to jointly handle the “trucks or telephones” from Heinlein’s short story[2](https://blog.gregbrockman.com/define-cto-openai#fn2). I feel incredible gratitude towards Ilya, Sam, Elon, and everyone else who is making OpenAI happen.

(Incidentally, it’s very possible to become one of the people who is making OpenAI happen — we’re [hiring](https://jobs.lever.co/openai). Our engineering projects vary widely, from infrastructure/reliability to abstraction design to distributed algorithm implementation to data visualization to dashboard creation. No machine learning background necessary. If you’re interested in AI but not quite ready to join, check out our [Requests for Research](https://openai.com/requests-for-research/).)
