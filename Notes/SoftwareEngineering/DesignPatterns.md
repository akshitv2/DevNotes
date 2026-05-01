---
parent: Programming Core
title: Design Patterns
nav_order: 2
layout: default
---

# Design Patterns

- Design patterns are typical solutions to commonly occurring problems in software design
- Types:
    - Creational
    - Structural
    - Behavioural

# Creational Patterns
- Creational design patterns provide various object creation mechanisms, which increase flexibility and reuse of existing code.

1. ### Factory 🟦IMPORTANT🟦<span style="background-color:red; color:white; padding:1px 4px; border-radius:2px; font-size:0.5em; font-weight:bold;">IMPORTANT</span>
    - Factory Design Pattern is a creational pattern that provides an interface for creating objects in a superclass but
      allows subclasses to alter the type of objects that will be created
    - .i.e You can have multiple implementations of same base class controlled through Factory which creates the product
    - ```java
      interface Shape {
        void draw();
      }
      
      class Circle implements Shape {
        @Override
        public void draw() {
            System.out.println("Drawing a Circle.");
        }
      }
      
      class Square implements Shape {
        @Override
        public void draw() {
            System.out.println("Drawing a Square.");
        }
      }
      
      class ShapeFactory {
        public Shape getShape(String shapeType) {
          if (shapeType == null) {
            return null;
          }
          if (shapeType.equalsIgnoreCase("CIRCLE")) {
            return new Circle();
          } else if (shapeType.equalsIgnoreCase("SQUARE")) {
            return new Square();
          }
          return null;
        }
      }
      ```
2. ### Abstract Factory <span style="background-color:red; color:white; padding:1px 4px; border-radius:2px; font-size:0.5em; font-weight:bold;">IMPORTANT</span>
3. ### Builder <span style="background-color:blue; color:white; padding:1px 4px; border-radius:2px; font-size:0.5em; font-weight:bold;">MODERATE</span>
    - Used to construct complex objects step by step
    - We extract the object construction code out of its own class and move it to separate objects called builders.
    - ```java
      public class Computer {
      // Required parameters
      private String HDD;
      private String RAM;
      
          // Optional parameters
          private boolean isGraphicsCardEnabled;
          private boolean isBluetoothEnabled;
      
          public String getHDD() { return HDD; }
          public String getRAM() { return RAM; }
          public boolean isGraphicsCardEnabled() { return isGraphicsCardEnabled; }
          public boolean isBluetoothEnabled() { return isBluetoothEnabled; }
      
          // Private constructor so only the Builder can instantiate it
          private Computer(ComputerBuilder builder) {
              this.HDD = builder.HDD;
              this.RAM = builder.RAM;
              this.isGraphicsCardEnabled = builder.isGraphicsCardEnabled;
              this.isBluetoothEnabled = builder.isBluetoothEnabled;
          }
      
          // Builder Class
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
      
      //Allows us to do this
      Computer comp = new Computer.ComputerBuilder("500 GB", "16 GB")
                .setGraphicsCardEnabled(true)
                .build();
      ```
4. ### Prototype <span style="background-color:blue; color:white; padding:1px 4px; border-radius:2px; font-size:0.5em; font-weight:bold;">FRINGE</span>
   - Design pattern that lets you copy existing objects without making your code dependent on their classes.
   - The Prototype pattern lets the actual object being cloned define its own cloning process
   - Abstract Prototype
     - ```java
       abstract class Shape implements Cloneable {
       private String id;
       protected String type;
       
           abstract void draw();
       
           public String getType() { return type; }
           public String getId() { return id; }
           public void setId(String id) { this.id = id; }
       
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
       ```
   - Concrete:
     - ```java
       class Rectangle extends Shape {
       public Rectangle() { type = "Rectangle"; }
       
           @Override
           public void draw() { System.out.println("Inside Rectangle::draw() method."); }
       }
       ```
5. ### Singleton <span style="background-color:red; color:white; padding:1px 4px; border-radius:2px; font-size:0.5em; font-weight:bold;">IMPORTANT</span>
    - Ensures that each class has a single instance
    - Usually used to control access to a shared resource
    - ```java
      public class DatabaseConnection {
      
          // Private constructor prevents instantiation from other classes
          private DatabaseConnection() {
              System.out.println("Connecting to Database...");
          }
      
          // Static inner class responsible for holding the instance
          private static class Holder {
              private static final DatabaseConnection INSTANCE = new DatabaseConnection();
          }
      
          public static DatabaseConnection getInstance() {
              return Holder.INSTANCE;
          }
      }
      ```
      
# Structural Patterns
1. ### Adapter <span style="background-color:red; color:white; padding:1px 4px; border-radius:2px; font-size:0.5em; font-weight:bold;">IMPORTANT</span>
   - Allows Objects with incompatible interfaces to work together
   - Uses a wrapper class i.e. the adapter that is extends the common interface
   - ```java
     interface MediaPlayer {
         void play(String audioType, String fileName);
     }
     
     //Incompatible Class
     class VlcPlayer {
         void playVlc(String fileName) {
             System.out.println("Playing vlc file: " + fileName);
         }
     }
     
     //Adapter
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
     
2. Bridge <span style="background-color:gray; color:white; padding:1px 4px; border-radius:2px; font-size:0.5em; font-weight:bold;">FRINGE</span>
3. Composite <span style="background-color:blue; color:white; padding:1px 4px; border-radius:2px; font-size:0.5em; font-weight:bold;">MODERATE</span>
4. Decorator <span style="background-color:blue; color:white; padding:1px 4px; border-radius:2px; font-size:0.5em; font-weight:bold;">MODERATE</span>
5. Facade <span style="background-color:blue; color:white; padding:1px 4px; border-radius:2px; font-size:0.5em; font-weight:bold;">MODERATE</span>
6. Flyweight <span style="background-color:gray; color:white; padding:1px 4px; border-radius:2px; font-size:0.5em; font-weight:bold;">FRINGE</span>
7. Proxy