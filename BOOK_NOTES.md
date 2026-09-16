# OOD, TDD, DDD, event-driven architecture


## Domain modeling and DDD (Building an Architecture to Support Domain Modeling)
The goal of the domain modeling is to started with a model that has no external dependencies, but has fast unit tests. We can keep the domain model easy to change and free of low-level concerns by choosing the right abstractions and continuously applying the DIP.

![tdd-ddd-event-driven](./tdd-ddd-event-driven.png)
1. OOD is core concept on design your codebase (including OOP terms, SOLID principles and other patterns like Repository?) while DDD is how you use those pieces of code (design) combining them to describe (model) the business elements (domains) and its relationships.
2. DDD is about building a good model of business domain / Event-driven to manage complexity about business domain.
3. Domain Driven Design combines design and development practice, and shows how design and development can work together to create a better solution.

## Repository, Service Layer, and Unit of Work patterns
These three closely related and mutually reinforcing patterns that support our ambition to keep the model free of extraneous dependencies. We build a layer of abstraction around persistent storage, and we build a service layer to define the entrypoints to our system and capture the primary use cases.

### SOLID principles
1. S - single responsibility: класс отвечает за конкретную работу (Square/Triangle/Circle, Output) и должна быть только одна причина для его изменения.
2. O - open-closed: класс д/б открыт для расширения но закртыт для изменений (если расширять то без модификация самого класса - реализовать свои методы вычисления площади для классов разных фигур квадрат, круг и так далее).
3. L - Liskov substitution: каждый производный класс может быть заменен своим родительским или базовым классом без поломки функциональности (класс Пенгвин унаследованный от Птица не должен падать при вызове метода fly следовательно нужно обеспечить дополнительный класс для не летающих птиц таких как пингвин/страус и др). Еще есть History rule: производный класс не должен изменять состояние объекта если это не заложено в родительском (ребенок-человек, но нельзя чтобы он мог летать).
4. I - interface segregation: нет необходимости в доп полях/методах для клиента если он ими не пользуется (пульт с кнопками только для ТВ, только кондиционера и т/д)
5. D - dependency inversion: зависимости должны строиться на абстракциях, а не на конкретных реализациях (хороший пример разделения на слои web/service/DB) см [DIP](#dependency-inversion-principle-dip)


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
Чтобы решить проблему по мере роста приложения чтобы избежать глобальных последствий внося изменения в систему принято разделять на слои:
Web/Presentation (API/CLI) --> Service/Business --> Data model is the pattern for building business apps

*Этот паттерн строится на принципе DIP!*

### Dependency Inversion Principle (DIP)
1. High-level modules (классы/функции и методы которые напрямую взаимодействуют с пользователем) should not depend on low-level modules. Both should depend on abstractions. Business code shouldn’t depend on technical details!
2. Abstractions should not depend on details. Instead, details
should depend on (знает о другом модуле или нуждается в нем) abstractions.

Абстракции - это упрощенные интерфейсы, которые инкапсулируют поведение (подобно тому как модуль
duckduckgo инкапсулировал API поисковой машины).


### Domain Model pattern - место для всей бизнес логики
Решает проблему с тем что бизнес логика (Service/Business layer) разбросана по другим слоям.
Следовательно нужно создавать этот т/н middle layer используя Domain Model pattern.

### patterns
These closely related and mutually reinforcing patterns that support our ambition to keep the model free of extraneous dependencies. 
OOD principles are the foundation for the repository and service layer patterns, which are specific architectural patterns used to organize object-oriented systems and enforce key design principles.

Four _key design patterns_ helps us to build a rich object model with persistence-ignorant code and to keep that model decoupled from technical concerns:

- Repository pattern - a layer of abstraction around persistent storage
- Service layer pattern - the entrypoints to our system, whether it’s a Flask/Fastapi API or a CLI. Also define use cases: where it begins and ends.
- Unit of Work pattern - обеспечивает атомарность ?операцям?
- The Aggregate pattern - ?обеспечение целостности данных? A DDD aggregate is a cluster of domain objects that can be treated as a single unit.

![component-diagram](./component-diagram-part-1.png)


# Domain Modeling
It answers the question: "how we can model business processes with code with TDD compatible way"?

use a few _key architecture patterns_ for modeling domains: 
1 Entity: identity equality, domain object that has long-lived identity
2 Value Object: value equality, domain object that can be idintified by its data itself, that has no long-livedidentity/UUID.
3 Domain Service

Мы заменяем термин business layer на термин __domain model__!

Бизнес говорит на языке сленга и жаргона принятого в отрасли - использует специфичные термины. Термины и жаргоны возникают естественным образом так как это способ описать сложную систему или процесс в одно-два слова или предложения в рамках бизнес-процесса.

Следовательно, Domain - это способ выражения задач бизнеса которую нужно решить в рамках конкретного процесса (закупка/дистрибьюция/склад/etc). Model - это карта процесса с полезными свойствами (property). The domain model is the mental map that business owners have of their businesses. 

Мы создаем т/н _ubiquitous language_ как это мост между business/technology. Мы пользуемся терминологией чтобы упростить коммуникацию и преодолеть сложности процессов опуская детали.

Модель начинается с понимания действий внутри модели в рамках ubiquitous language, в первой итерации мы создаем ключевые объекты взаимодействия: Order/OrderLine/Batch. Далее начинаем думать над валидацией входных данных через призму предложений/messages/jargons:
- Заказ должен иметь ID/SKU, quantity/qty, reference/ref
- Не может быть одинаковых заказов в одину и туже партию/Batch и т/д

### Unit testing - TDD
We construct a model from this business conversation by using TDD approach.

1. Also we need to know about __Value object pattern__: when we can identify object by the internal data it represent/store we ca say that it is _Value Object_! So, 
a __value object__ is any domain object that is uniquely identified by the data it holds, and `dataclass` helps us by providing `__eq__` mothod internally (providing object comparisons),
Dataclasses Are Great for Value Objects because it is _value equality_!

In fact, it’s common to support operations on values, for example
![math with Value objects](./value-obj-math.png)

```python
@dataclass(frozen=True)
"""For value objects, the hash should be based on all the value attributes,
and we should ensure that the objects are immutable. We get this for
free by specifying @frozen=True on the dataclass that guarantee immutability 
(do not need to define hash or eq methods).
"""
class Name:
    firstname: str
    secondname: str
# Name is the Value Object because if any property will changed we got new value
assert Name("Kirill", "Zhdanov") != Name("Kirill", "Sarksyan")

from typing import NamedTuple
class Money(NamedTuple):
    currency
    amount
# Money is the Value Object
assert Money('gbp', 10) == Money('gbp', 10)
assert Money('gbp', 10) != Money('gbp', 15)
```

2. We use term _entity_ (__entity pattern__) to identify domain object that has long-lived identity. So, entities unlike values have _identity equality_ (compares identities)!
We can change their values, and they are still recognizably the same thing. We usually make this explicit in code by implementing equality operator on entities:

```python
class Batch:
    ...
    def __eq__(self, other):
        """to support `==` operator on instances (define the behavior of the class for == operator)
        By default, compares two instances by their identity – therefore instances are only equal to themselves, meaning...
        
        https://docs.python.org/3/reference/datamodel.html#object.__eq__
        https://docs.python.org/3/reference/expressions.html#value-comparisons
        https://docs.python.org/3/reference/expressions.html#is-not
        
        ...by default, meaning all objects compare unequal (except with themselves), so, by default, compares identities:
            def __eq__(self, other):
                return self is other  # Сравнивает именно id(self) == id(other)

        The operators is and is not test for an object’s identity: `x is y` is true if and only if x and y are the same object. An Object’s identity is determined using the id() function.

        https://docs.python.org/3/reference/datamodel.html#objects
        For CPython, id(x) is the memory address where x is stored.
        """
        if not isinstance(other, Batch):
            return False
        # but it case of IDENTITY equality we specify wich UUID we equals by to recognize any Person as individual whatever name they holds, so that defines the entity’s unique identity over time
        return other.reference == self.reference

    def __hash__(self):
        """This magic method Python uses to control the behavior of
        objects when you add them to sets or use them as dict keys

        https://docs.python.org/3/reference/datamodel.html#object.__hash__

        The __hash__() method should return an integer. 
        The only required property is that objects which compare equal have the same hash value.

        If a class does not define an __eq__() method it should not define a __hash__() operation either; 
        if it defines __eq__() but not __hash__(), its instances will not be usable as items in hashable collections.
        """
        return hash(self.reference)
```

3. A Domain Service represents a business concept or process, whereas a service-layer service represents a use case for your application. Given set of batches, we need to allocate OrderLine from it!

Validation is about the preconditions: syntax, semantics, and pragmatics!
