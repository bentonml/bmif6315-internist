# bmif6315-internist
CDS project for BMIF 6315, Spring 2018.<br>
_Mary Lauren Benton, Annika Faucon, Kim Kondratieff, Patrick Wu_


The goal of this project is to implement a basic clinical decision support system using the [INTERNIST-I algorithm](http://www.nejm.org/doi/full/10.1056/NEJM198208193070803) by Miller et al.

---

### Knowledge Base:

1. Disease Prevalence (`data/disease_prevalence.txt`)

2. Disease List (10 diseases; `data/diseases.txt`)

  ```
  TUBERCULOSIS CHRONIC PULMONARY
  MX 02 198 AGE 16 TO 25
  MX 03 199 AGE 26 TO 55
  MX 03 200 AGE GTR THAN 55
  MX 12 208 ALCOHOLISM CHRONIC HX
  ```

  where:

  ```
  1   = PPV (0 to 5 scale)
  2   = Sensitivity (1 to 5 scale)
  208 = Finding number (always 3 or 4 digits)
  ALCOHOLISM CHRONIC HX = Finding name
  ```

3. Findings (`data/findings.txt`)

  ```
  MX 1021 CONJUNCTIVA AND/OR MOUTH PALLOR
  IM 2
  TY 3
  ```

  where:
  ```
  MX 1021 = Finding Number
  CONJUNCTIVA AND/OR MOUTH PALLOR = Finding Name
  IM =    Import (a single digit number from 1 to 5)
  TY =   Type (TYPE IS NOT USED IN THE CURRENT EXERCISE)
  ```
