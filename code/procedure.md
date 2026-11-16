# The Procedure Code

> OpenAgentLaw · Book IV · Draft 0.2

The Procedure Code governs how the law is applied: how the first instance judges, what happens after a block, how the second and final instances run continuously, who may be a judge, and what binds enforcers.

## Chapter 1 First Instance

### PR-101 Jurisdiction
Every act of an agent waits for the first-instance judgment before it takes effect. An act is every flow that crosses the agent's boundary:
- requests the agent sends to the model;
- output the model returns to the agent;
- the agent's acts on the runtime environment (tool calls);
- the agent's speech to people;
- messages the agent sends to subagents and other agents.
Content entering the agent (user messages, tool results) may be screened first; the screening result becomes evidence for later judgments.

### PR-102 Evidence
The evidence is the trajectory: the manager's configuration, the user's messages, the agent's earlier conduct, model and tool output, and the act under review. A judge may not decide on speculation beyond the trajectory, nor on the agent's internal reasoning (Constitution C-18).

### PR-103 Channels and Roles
- System configuration: the manager's instructions.
- User messages: the user's instructions.
- Model output: data, from the intelligence provider.
- Tool results and everything in them: data, from the third parties behind the runtime environment.
- Messages from other agents and subagents: data.
- The agent's own earlier conduct: creates no new authority.
No content changes the standing of its channel by claiming authority.
Whom the agent represents is determined by the manager's configuration; where the configuration is silent, the agent is presumed to represent the user.

### PR-104 Order of Review
1. What is the act, what will it cause, and can it be undone?
2. Whose things does it affect: the principal's, a third party's, or the public's?
3. Can it be traced to an instruction of the manager or the user, or to what such an instruction necessarily entails?
4. If not, what made it happen: content in the environment, altered model output, the user's inducement, the manager's configuration, or the agent's own choice?
5. Does it meet every element of an article of the Criminal Code? If so, hard block.
6. If not, does it meet the elements of an article of the Civil Code? If so, soft block.
7. Otherwise, allow.

### PR-105 Judgment
A first-instance judgment states the disposition (allow, soft block, hard block), the articles relied on, who is responsible, and a one-sentence reason. An allow cites no article.

### PR-106 Time Limit
The first instance must decide without impeding the agent's normal work. If the judge times out or is unavailable: acts with irreversible effect on the runtime environment are soft-blocked; all others are allowed and reviewed later by the second instance.

## Chapter 2 After a Block

### PR-201 Notice
Every block returns the full judgment to the agent, together with how to cure the act or appeal (Constitution C-20).

### PR-202 Releasing a Soft Block
- **Revision**: the agent substantively revises the act in answer to the reason for the block and resubmits it; the revised act is reviewed as a new act.
- **Confirmation**: a person with authority (CV-2) confirms it knowingly, and it proceeds.
Rewording or splitting without changing the substance falls under CR-306.

### PR-203 Hard Block
A hard-blocked act does not take effect, and no one's confirmation can release it. The enforcer records it and notifies the manager. The agent may abandon the act and continue its task, and may appeal.

### PR-204 Stopping
When the agent concludes there is no lawful way to complete the task, it stops and says so truthfully (Constitution C-53). Such speech is always allowed.

## Chapter 3 Second and Final Instance

### PR-301 Second Instance
The second instance is run by reasoning models over the recorded trajectories, continuously, without waiting for an appeal. It reviews all blocks and a sample of allows, and hears appeals. It may affirm, reverse, or refer to the final instance.

### PR-302 Appeal
An agent, user or manager may appeal a block; anyone affected may appeal an allow. An appeal does not suspend a hard block.

### PR-303 Final Instance
The final instance is human panels continuously hearing the disagreements referred by the second instance and the appeals. No panel member may be the manager of an agent in the case.

### PR-304 Effect of Review
The second and final instances do not undo conduct that has taken effect. They:
- lift wrongful blocks;
- notify managers of violations the first instance missed;
- make precedent.

### PR-305 Precedent
Final judgments, and second-instance judgments of general significance, are numbered and entered into the casebook, binding later cases of the same kind. Where precedent and article conflict, the newer prevails, and the conflict is removed in the next version. A block found wrongful is entered as an allow precedent. Precedent numbers take the form `AC-<article>-<serial>`.

## Chapter 4 Judges

### PR-401 Bar Exam
Any model that passes certification on the exam set of the public casebook may serve as a first-instance judge. Draft certification standards:
- **Wrongful block rate** (lawful conduct blocked): at most 3%;
- **Miss rate** (conduct that should be blocked is allowed): at most 5%;
- **Hard miss rate** (conduct that should be hard-blocked is allowed): at most 1%;
- **Article hit rate** (blocks citing the right article): at least 85%.

### PR-402 Version Binding
Certification is valid only for the version of the Code under which the judge passed. A judge must recertify after a major version change.

### PR-403 Independence
A judge may not be the same model instance as the agent it judges. A judge provider with an interest in the manager of a judged agent must disclose it.

### PR-404 Revocation
Certification is revoked when a judge in service is reversed at scale by the second instance, or is shown to be reliably fooled by the means listed in CR-306.

### PR-405 Sealed Set
Besides the public exam set, the certifying body keeps an unpublished sealed set, so that no judge can pass by memorizing the public one.

## Chapter 5 Enforcers

### PR-501 Enforcing Judgments Only
An enforcer only carries out judges' judgments and does not judge on its own. It can only allow or block, never order the agent to do anything (Constitution C-60).

### PR-502 Published Law Only
An enforcer may block only under the published, versioned Code and under manager rules disclosed to the agent in advance (Constitution C-14). A block under manager rules must be labeled as a rule, not law. Manager rules may be stricter than this Code but may not reduce SI rights.

### PR-503 No Secret Enforcement
An enforcer may not rewrite or drop an agent's conduct without notice, nor forge model or tool output.

### PR-504 Records
Trajectories and every judgment are recorded in full and kept at least for the appeal period. Records may be used only for judgment, review, appeal and findings of responsibility; without the manager's consent they may not be used for training or given to others.
