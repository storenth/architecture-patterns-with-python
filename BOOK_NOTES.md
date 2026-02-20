# OOD, TDD, DDD, event-driven architecture

## Domain modeling and DDD (Building an Architecture to Support Domain Modeling)
The goal of the domain modeling is to started with a model that has no external dependencies, but has fast unit tests.
![tdd-ddd-event-driven](./tdd-ddd-event-driven.png)
1. OOD is core concept on design your codebase (including OOP terms, SOLID principles and other patterns like Repository?) while DDD is how you use those pieces of code (design) combining them to describe (model) the business elements (domains) and its relationships.
2. DDD is about building a good model of business domain / Event-driven to manage complexity about business domain.
3. Domain Driven Design combines design and development practice, and shows how design and development can work together to create a better solution.

### SOLID principles
1. S - single responsibility: класс отвечает за конкретную работу (Square/Triangle/Circle, Output) и должна быть только одна причина для его изменения.
2. O - open-closed: класс д/б открыт для расширения но закртыт для изменений (если расширять то без модификация самого класса - реализовать свои методы вычисления площади для классов разных фигур квадрат, круг и так далее).
3. L - Liskov substitution: каждый производный класс может быть заменен своим родительским или базовым классом без поломки функциональности (класс Пенгвин унаследованный от Птица не должен падать при вызове метода fly следовательно нужно обеспечить дополнительный класс для не летающих птиц таких как пингвин/страус и др). Еще есть History rule: производный класс не должен изменять состояние объекта если это не заложено в родительском (ребенок-человек, но нельзя чтобы он мог летать).
4. I - interface segregation: нет необходимости в доп полях/методах для клиента если он ими не пользуется (пульт с кнопками только для ТВ, только кондиционера и т/д)
5. D - dependency inversion: зависимости должны строиться на абстракциях, а не на конкретных реализациях (хороший пример разделения на слои web/service/DB) см [DIP](#dependency-inversion-principle-dip)


### patterns
These closely related and mutually reinforcing patterns that support our ambition to keep the model free of extraneous dependencies. 
OOD principles are the foundation for the repository and service layer patterns, which are specific architectural patterns used to organize object-oriented systems and enforce key design principles
- Repository pattern - a layer of abstraction around persistent storage
- Service layer pattern - the entrypoints to our system: thin entrypoints to our system, whether it’s a Flask/Fastapi API or a CLI.
- Unit of Work pattern

## Event-Driven architecture
Solution to solve временную связность problem.
three more mutually reinforcing patterns: the Domain Events, Message Bus, and Handler patterns:
- Domain Events pattern - interactions with a system triggers for other interactions
- Message bus - allow actions (interactions) to trigger Events and call appropriate Handlers
Events can be used as a pattern for integration between services in a microservices architecture


# Intro
For scientists, though, chaos is characterized by homogeneity (гомогенность/одинаковость/sameness), and order by complexity (отличием/difference - потому что разные объекты должны быть упорядочены и разграничены между собой).

## Encapsulation and Abstractions
Инкапсуляция упрощает методы взаимодействия - упрощают поведение и сокрывают детали реализации. Инкапсулируя поведение мы создаем объект взаимодействия с системой - это пример абстракции. Стремление к higher-level of abstraction (на примере перехода от urllib к requests к использованию библиотеки duckduckgo) создает предпосылки для Encapsulating behavior by using abstractions is a powerful tool for making code more expressive, more testable, and easier to maintain.

### three-layered architecture pattern
Web/Presentation --> Service/Business --> Data model is the pattern for building business apps
Этот паттерн строится на принципе DIP

### Dependency Inversion Principle (DIP)
1. High-level modules (классы/функции и методы которые напрямую взаимодействуют с пользователем) should not depend on low-level modules. Both should depend on abstractions. Business code shouldn’t depend on technical details!
2. Abstractions should not depend on details. Instead, details
should depend on (знает о другом модуле или нуждается в нем) abstractions.

Абстракции - это упрощенные интерфейсы, которые инкапсулируют поведение (подобно тому как модуль
duckduckgo инкапсулировал API поисковой машины)

### Domain Model pattern - место для всей бизнес логики
Решает проблему с тем что бизнес логика (Service/Business layer) разбросан по другим слоям.
Следовательно нужно создавать этот т/н middle layer используя Domain Model pattern

# Domain Modeling
