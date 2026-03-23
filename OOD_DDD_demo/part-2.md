OOD, DDD, event-driven architecture 2/N [DIP]



Lets try to understand one noted simple principle in "part 1/N [intro]" - Dependency inversion principle: https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design#dependency-inversion-principle



"It states that the high-level module must not depend on the low-level module, but they should depend on abstractions." One more time we faced with Abstraction!



It is the core concept, look at the snippet: the left side of the code example show us that we directly use (depends on) low-level implementation (MySQLConnection) and violates that principle: if we change DB connector later we must also fix PasswordReminder class.



So we can create an interface to follow the DIP statement to encapsulate and isolate both behavior. Abstraction is the simplified interface that encapsulates behavior! Adding an abstraction between the low and high mudules allows to non-destructively change them, independently of each other.



This simple example shows us how applying the DIP drive Layered architecture pattern (three-tier-model) on different point of view: inside layers and between layers. Now we need to focused on service/business/middle layer because is the most valuable part of the app, and in the next parts I will write how to build a business layer with a Domain Model pattern to keep it free of low level details and dependencies.