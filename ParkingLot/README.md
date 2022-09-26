# Low Level System Design - Parking lot 
### Python Machine Code



---

#### Original Java Solution by [Udit Agarwal](https://youtu.be/7IX84K9g23U)
#### Follow Udit Agarwal [Linkedin](https://www.linkedin.com/in/anomaly2104/)

---
### Problem Statement
[Check here](problem-statment.md)

  

### Further Enhancements:

* Dependency injection: Currently dependencies are injected manually. We can use some 
dependency injection framework like spring. 
* Exit command: Exit command is currently coupled with interactive mode only which makes
it non-reusable.
* Parking strategy: Parking strategy is currently associated with `ParkingLotService`. 
Instead of that, it makes more sense to associate it with `ParkingLot`.
* Mode: Mode checking is currently done in main function directly. There could be a
factory for that.

---
#### If you find it helpful add me on [Linkedin](https://www.linkedin.com/in/akshansh-gusain-23023374/)