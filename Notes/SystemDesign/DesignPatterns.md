# Design Patterns

Design patterns are typical, reusable solutions to commonly occurring software design problems. They fall into three
main categories:

* **Creational:** Object creation mechanisms that increase code flexibility and reuse.
* **Structural:** Structures for assembling objects and classes into larger, flexible configurations.
* **Behavioral:** Patterns concerned with algorithms and the assignment of responsibilities between objects.

---

## Quick Reference

### Creational Patterns

* **🔴[Singleton](#5-singleton-critical):** Restricts a class to a single instance while providing global access to it.
* **🔴[Factory Method](#1-factory-method-critical):** Provides an interface for creating objects, delegating
  instantiation logic to subclasses.
* **🟠[Abstract Factory](#2-abstract-factory-critical):** Creates families of related or dependent objects without
  specifying their concrete classes.
* **🔴[Builder](#3-builder-moderate):** Constructs complex objects step-by-step, separating construction from
  representation.
* **🟡[Prototype](#4-prototype-fringe):** Creates new objects by cloning an existing configured instance.

### Structural Patterns

* **🔴[Adapter](#1-adapter-critical):** Allows objects with incompatible interfaces to collaborate via a wrapper
  interface.
* **🟡[Bridge](#2-bridge-fringe):** Decouples an abstraction from its implementation so both can vary independently.
* **🟠[Composite](#3-composite-moderate):** Treats individual objects and object compositions uniformly using a tree
  structure.
* **🟠[Decorator](#4-decorator-moderate):** Attaches additional responsibilities to an object dynamically without
  modifying its base code.
* **🟠[Facade](#5-facade-moderate):** Offers a simplified, high-level interface to a complex system of classes or
  libraries.
* **🟡[Flyweight](#6-flyweight-fringe):** Reduces memory footprint by sharing common parts of state across multiple
  objects.
* **🟠[Proxy](#7-proxy-moderate):** Provides a placeholder or gatekeeper to control access, caching, or logging for
  another object.

### Behavioral Patterns

* **🔴[Chain of Responsibility](#1-chain-of-responsibility-critical):** Passes a request along a chain of handlers until
  one processes it.
* **🔴[Command](#2-command-critical):** Encapsulates a request as an object packaging its own data as well as code,
  enabling queuing, logging, and undo
  operations.
* **[Interpreter](#behavioral-patterns):** Evaluates language grammar or expressions for a defined representation.
* **🔴[Iterator](#3-iterator-critical):** Sequentially accesses elements of a collection without exposing its underlying
  structure.
* **🟠[Mediator](#4-mediator-moderate):** Centralizes complex communications and control flow between interdependent
  objects.
* **🟡[Memento](#5-memento-fringe):** Captures and restores an object's internal state without violating encapsulation.
* **🔴[Observer](#6-observer-critical):** Defines a subscription mechanism to notify multiple objects of state changes.
* **[State](#7-state-critical):** Permits an object to alter its behavior when its internal state changes.
* **[Strategy](#8-strategy-critical):** Encapsulates interchangeable algorithms behind a single interface to swap them
  at runtime.
* **[Template Method](#9-template-method-critical):** Defines the skeleton of an algorithm in a base class, delegating
  specific steps to subclasses.
* **[Visitor](#10-visitor-fringe):** Separates an algorithm from the object structure on which it operates.

---

## Creational Patterns

### 1. Factory Method `[CRITICAL]`

Provides an interface for object creation in a superclass while allowing subclasses to alter the type of objects that
are instantiated.

* **Key Concept:** Defers instantiation logic to concrete subclasses. The caller remains decoupled from the specific
  class implementation.

```java
// Abstract Creator
abstract class ShapeFactory {
    public abstract Shape createShape();

    // Business logic dependent on object creation
    public void render() {
        Shape shape = createShape();
        shape.draw();
    }
}

// Concrete Creators
class CircleFactory extends ShapeFactory {
    @Override
    public Shape createShape() {
        return new Circle();
    }
}

class SquareFactory extends ShapeFactory {
    @Override
    public Shape createShape() {
        return new Square();
    }
}

```

---

### 2. Abstract Factory `[CRITICAL]`

Enables the creation of families of related objects without specifying their concrete classes.  
Think of it as a factory of factories operating across multiple dimensions (e.g., cross-platform UI suites).
Essentially if you have related classes (like ui elements) and you want to enforce creation to a common category (mac
os) then you employ this.

```python
from abc import ABC, abstractmethod


# Abstract Products
class Button(ABC):
    @abstractmethod
    def render(self) -> str: pass


class Checkbox(ABC):
    @abstractmethod
    def render(self) -> str: pass


# Concrete Products
class WinButton(Button):
    def render(self) -> str: return "Render Windows Button"


class WinCheckbox(Checkbox):
    def render(self) -> str: return "Render Windows Checkbox"


class MacButton(Button):
    def render(self) -> str: return "Render macOS Button"


class MacCheckbox(Checkbox):
    def render(self) -> str: return "Render macOS Checkbox"


# Abstract Factory
class GUIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button: pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox: pass


# Concrete Factories
class WinFactory(GUIFactory):
    def create_button(self) -> Button: return WinButton()

    def create_checkbox(self) -> Checkbox: return WinCheckbox()


class MacFactory(GUIFactory):
    def create_button(self) -> Button: return MacButton()

    def create_checkbox(self) -> Checkbox: return MacCheckbox()


# Client Code
def build_ui(factory: GUIFactory):
    button = factory.create_button()
    checkbox = factory.create_checkbox()
    print(button.render())
    print(checkbox.render())


# Usage
build_ui(WinFactory())

```

---

### 3. Builder `[MODERATE]`

Separates complex object construction from its representation, allowing the same construction process to create
different configurations step-by-step.

```java
public class Computer {
    // Required parameters
    private String HDD;
    private String RAM;

    // Optional parameters
    private boolean isGraphicsCardEnabled;
    private boolean isBluetoothEnabled;

    public String getHDD() {
        return HDD;
    }

    public String getRAM() {
        return RAM;
    }

    public boolean isGraphicsCardEnabled() {
        return isGraphicsCardEnabled;
    }

    public boolean isBluetoothEnabled() {
        return isBluetoothEnabled;
    }

    private Computer(ComputerBuilder builder) {
        this.HDD = builder.HDD;
        this.RAM = builder.RAM;
        this.isGraphicsCardEnabled = builder.isGraphicsCardEnabled;
        this.isBluetoothEnabled = builder.isBluetoothEnabled;
    }

    public static class ComputerBuilder {
        private String HDD;
        private String RAM;
        private boolean isGraphicsCardEnabled;
        private boolean isBluetoothEnabled;

        public ComputerBuilder(String hdd, String ram) {
            this.HDD = hdd;
            this.RAM = ram;
        }

        public ComputerBuilder setGraphicsCardEnabled(boolean isGraphicsCardEnabled) {
            this.isGraphicsCardEnabled = isGraphicsCardEnabled;
            return this;
        }

        public ComputerBuilder setBluetoothEnabled(boolean isBluetoothEnabled) {
            this.isBluetoothEnabled = isBluetoothEnabled;
            return this;
        }

        public Computer build() {
            return new Computer(this);
        }
    }
}

// Usage
Computer comp = new Computer.ComputerBuilder("500 GB", "16 GB")
        .setGraphicsCardEnabled(true)
        .build();

```

---

### 4. Prototype `[FRINGE]`

Allows copying existing objects without making client code dependent on their explicit concrete classes.

```java
// Abstract Prototype
abstract class Shape implements Cloneable {
    private String id;
    protected String type;

    abstract void draw();

    public String getType() {
        return type;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    @Override
    public Object clone() {
        Object clone = null;
        try {
            clone = super.clone();
        } catch (CloneNotSupportedException e) {
            e.printStackTrace();
        }
        return clone;
    }
}

// Concrete Prototype
class Rectangle extends Shape {
    public Rectangle() {
        type = "Rectangle";
    }

    @Override
    public void draw() {
        System.out.println("Inside Rectangle::draw() method.");
    }
}

```

---

### 5. Singleton `[CRITICAL]`

Ensures a class has only one global instance while providing a unified access point to it.

```java
public class DatabaseConnection {

    private DatabaseConnection() {
        System.out.println("Connecting to Database...");
    }

    // Lazy Initialization Holder Class Thread-Safe Idiom
    private static class Holder {
        private static final DatabaseConnection INSTANCE = new DatabaseConnection();
    }

    public static DatabaseConnection getInstance() {
        return Holder.INSTANCE;
    }
}

```

---

## Structural Patterns

### 1. Adapter `[CRITICAL]`

Converts the interface of a class into another interface expected by the client. Enables incompatible interfaces to work
together.

```java
interface MediaPlayer {
    void play(String audioType, String fileName);
}

// Incompatible Legacy/External Class
class VlcPlayer {
    void playVlc(String fileName) {
        System.out.println("Playing vlc file: " + fileName);
    }
}

// Adapter Wrapper
class MediaAdapter implements MediaPlayer {
    private VlcPlayer vlcPlayer;

    public MediaAdapter() {
        this.vlcPlayer = new VlcPlayer();
    }

    @Override
    public void play(String audioType, String fileName) {
        if (audioType.equalsIgnoreCase("vlc")) {
            vlcPlayer.playVlc(fileName);
        }
    }
}

```

---

### 2. Bridge `[FRINGE]`

Decouples a high-level abstraction from its low-level implementation, allowing both hierarchies to develop independently
via delegation.

```java
// Implementation Interface
public interface Device {
    boolean isEnabled();

    void enable();

    void disable();

    void setVolume(int percent);

    int getVolume();
}

// Concrete Implementations
public class Radio implements Device {
    private boolean on = false;
    private int volume = 30;

    @Override
    public boolean isEnabled() {
        return on;
    }

    @Override
    public void enable() {
        on = true;
    }

    @Override
    public void disable() {
        on = false;
    }

    @Override
    public void setVolume(int v) {
        this.volume = v;
    }

    @Override
    public int getVolume() {
        return volume;
    }
}

// Abstraction
public class RemoteControl {
    protected Device device; // The "Bridge"

    public RemoteControl(Device device) {
        this.device = device;
    }

    public void togglePower() {
        if (device.isEnabled()) {
            device.disable();
        } else {
            device.enable();
        }
    }

    public void volumeDown() {
        device.setVolume(device.getVolume() - 10);
    }

    public void volumeUp() {
        device.setVolume(device.getVolume() + 10);
    }
}

```

---

### 3. Composite `[MODERATE]`

Composes objects into tree structures to represent part-whole hierarchies. Enables clients to treat individual objects
and compositions uniformly.

```java
interface Node {
    void print();
}

class Leaf implements Node {
    private String name;

    Leaf(String name) {
        this.name = name;
    }

    public void print() {
        System.out.println(name);
    }
}

class Composite implements Node {
    private List<Node> children = new ArrayList<>();

    void add(Node n) {
        children.add(n);
    }

    public void print() {
        children.forEach(Node::print);
    }
}

// Usage
public class Main {
    public static void main(String[] args) {
        Composite root = new Composite();
        root.add(new Leaf("Leaf A"));

        Composite sub = new Composite();
        sub.add(new Leaf("Leaf B"));

        root.add(sub);
        root.print(); // Uniform execution across tree nodes
    }
}

```

---

### 4. Decorator `[MODERATE]`

Attaches additional responsibilities to an object dynamically. Provides a flexible alternative to subclassing for
extending functionality.

- It might be better to use a builder when the order doesn't matter otherwise you end up with this

```java
Coffee drink = new SugarPump(
        new SugarPump(
                new PumpkinSpice(
                        new SoyMilk(
                                new NonFatBase(
                                        new Espresso()
                                )
                        )
                )
        );
```

Useful here: `new BufferedReader(new GZIPInputStream(new FileInputStream(file))))`

```java
interface Coffee {
    double cost();
}

class SimpleCoffee implements Coffee {
    public double cost() {
        return 2.0;
    }
}

// Abstract Decorator
abstract class CoffeeDecorator implements Coffee {
    protected Coffee coffee;

    public CoffeeDecorator(Coffee c) {
        this.coffee = c;
    }

    public double cost() {
        return coffee.cost();
    }
}

// Concrete Decorator
class Milk extends CoffeeDecorator {
    public Milk(Coffee c) {
        super(c);
    }

    @Override
    public double cost() {
        return super.cost() + 0.5;
    }
}

```

---

### 5. Facade `[MODERATE]`

Provides a simplified interface to a complex subsystem of classes, library, or framework.

```java
// Subsystems
class Audio {
    void on() {
        System.out.println("Audio on");
    }
}

class Video {
    void on() {
        System.out.println("Video on");
    }
}

// Facade
class CinemaFacade {
    private Audio audio = new Audio();
    private Video video = new Video();

    public void play() {
        audio.on();
        video.on();
    }
}

// Client
public class Main {
    public static void main(String[] args) {
        new CinemaFacade().play(); // Simplified entry point
    }
}

```

---

### 6. Flyweight `[FRINGE]`

Reduces memory usage by sharing common constant parts of state across multiple instances instead of keeping identical
data inside each object.

---

### 7. Proxy `[MODERATE]`

Provides a placeholder or surrogate control layer for another object to inspect, log, cache, or control access to it.

```java
interface Subject {
    void request();
}

class RealSubject implements Subject {
    public void request() {
        System.out.println("RealSubject: Handling request.");
    }
}

class Proxy implements Subject {
    private RealSubject realSubject;

    public void request() {
        if (realSubject == null) {
            realSubject = new RealSubject(); // Lazy initialization
        }
        System.out.print("Proxy: Logging access prior to call - ");
        realSubject.request();
    }
}

```

---

## Behavioral Patterns

### 1. Chain of Responsibility `[CRITICAL]`

Passes requests along a sequential chain of potential handlers until one processes the request. (e.g., Spring Security
Filters).

---

### 2. Command `[CRITICAL]`

Encapsulates a request as an independent object, parameterizing clients with different requests, queueing executions,
and enabling undo operations.

```java
// 1. Command Interface
interface Command {
    void execute();
}

// 2. Receiver
class Light {
    void turnOn() {
        System.out.println("Light is ON");
    }
}

// 3. Concrete Command
class LightOnCommand implements Command {
    private Light light;

    public LightOnCommand(Light light) {
        this.light = light;
    }

    public void execute() {
        light.turnOn();
    }
}

// 4. Invoker
class RemoteControl {
    private Command slot;

    public void setCommand(Command command) {
        slot = command;
    }

    public void pressButton() {
        slot.execute();
    }
}

// Client
public class Main {
    public static void main(String[] args) {
        Light light = new Light();
        Command lightOn = new LightOnCommand(light);

        RemoteControl remote = new RemoteControl();
        remote.setCommand(lightOn);
        remote.pressButton();
    }
}

```

* **Trade-off:** Decouples invokers from receivers but increases class proliferation (a separate class per command
  action).

---

### 3. Iterator `[CRITICAL]`

Provides a uniform strategy to access elements of an aggregate collection sequentially without exposing its underlying
internal representation.

---

### 4. Mediator `[MODERATE]`

Restricts direct communications between objects by forcing all collaboration to route through a single mediator
component thus removing N to N coupling, channeling flow of data through mediator

---

### 5. Memento `[FRINGE]`

Captures and externalizes an object's internal state so that it can be restored later without violating encapsulation (
used for undo operations).
Basically you pass in a nested class which holds the Stack/Array of changes.

---

### 6. Observer `[CRITICAL]`

Defines a one-to-many dependency relationship so that when one object changes state, all registered dependents are
notified automatically (Publisher/Subscriber model).

* **Push Model:** Publisher forces state payloads out to all subscribers.
* **Pull Model:** Publisher notifies subscribers, and subscribers pull data on demand.
* **Note:** Unlike message queues operating asynchronously via polling, traditional standard Observers are temporally
  coupled (publisher and subscriber must execute concurrently).

---

### 7. State `[CRITICAL]`

Allows an object to alter its behavior when its internal state changes, making it appear as if the object changed its
class. Replaces conditional statements (`if/else`, `switch`) with polymorphic state objects.

```java
// State Interface
interface State {
    void handle(LightSwitch context);
}

// Concrete States
class OnState implements State {
    public void handle(LightSwitch context) {
        System.out.println("Turning light OFF.");
        context.setState(new OffState());
    }
}

class OffState implements State {
    public void handle(LightSwitch context) {
        System.out.println("Turning light ON.");
        context.setState(new OnState());
    }
}

// Context
class LightSwitch {
    private State state = new OffState(); // Initial state

    public void setState(State state) {
        this.state = state;
    }

    public void press() {
        state.handle(this);
    }

    public static void main(String[] args) {
        LightSwitch light = new LightSwitch();
        light.press(); // Turning light ON.
        light.press(); // Turning light OFF.
    }
}

```

* **Transition Ownership:** Transitions can reside either within **Concrete States** (self-transitioning) or within the
  **Context** class.

---

### 8. Strategy `[CRITICAL]`

Defines a family of interchangeable algorithms, encapsulates each one, and makes them plug-and-playable at runtime.

```java
interface PaymentStrategy {
    void pay(int amount);
}

class CreditCardPayment implements PaymentStrategy {
    public void pay(int amount) {
        System.out.println("Paid " + amount + " using Credit Card.");
    }
}

class PaypalPayment implements PaymentStrategy {
    public void pay(int amount) {
        System.out.println("Paid " + amount + " using PayPal.");
    }
}

class ShoppingCart {
    private PaymentStrategy strategy;

    public void setPaymentStrategy(PaymentStrategy strategy) {
        this.strategy = strategy;
    }

    public void checkout(int amount) {
        strategy.pay(amount);
    }
}

public class Main {
    public static void main(String[] args) {
        ShoppingCart cart = new ShoppingCart();

        cart.setPaymentStrategy(new CreditCardPayment());
        cart.checkout(100);

        cart.setPaymentStrategy(new PaypalPayment());
        cart.checkout(200);
    }
}

```

---

### 9. Template Method `[CRITICAL]`

Defines the invariant step framework of an algorithm in a base class method while allowing subclasses to override
specific step implementations.

```java
abstract class DataMiner {
    // Template Method: Skeleton process fixed via 'final'
    public final void mineData() {
        openFile();
        extractData(); // Deferred to subclass
        parseData();   // Deferred to subclass
        closeFile();
    }

    private void openFile() {
        System.out.println("Opening file...");
    }

    private void closeFile() {
        System.out.println("Closing file...");
    }

    protected abstract void extractData();

    protected abstract void parseData();
}

```

* **Limitation:** Creates tight inheritance coupling between the base class contract and extending subclasses.

---

### 10. Visitor `[FRINGE]`

Separates algorithms from the objects on which they operate by passing visitor objects into element structure nodes.

```

```