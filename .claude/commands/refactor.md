--- 

description: Refactor a file with a stated goal, keeping behaviour identical 

argument-hint: [file] [goal] 

--- 

  

Refactor $1 with this goal: $2 

  

Constraints: 

  

- Behaviour must not change. The public function names stay the same. 

- Every existing test must still pass, unmodified. 

- Do not add dependencies. 

  

First show me a plan. Do not change anything until I approve it. 