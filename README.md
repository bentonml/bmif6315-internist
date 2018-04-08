# bmif6315-internist
CDS project for BMIF 6315, Spring 2018.<br>
_Mary Lauren Benton, Annika Faucon, Kim Kondratieff, Patrick Wu_


The goal of this project is to implement a basic clinical decision support system using the [INTERNIST-I algorithm](http://www.nejm.org/doi/full/10.1056/NEJM198208193070803) by Miller et al.

---

### Knowledge Base:

We'll use the disease list and findings table for this implementation. The disease prevalence table is not required.

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
  1   = PPV (0 to 5 scale) = evoking strength  (*)
  2   = Sensitivity (1 to 5 scale) = frequency (*)
  208 = Finding number (always 3 or 4 digits)
  ALCOHOLISM CHRONIC HX = Finding name
  ```

  Removed all trailing whitespace from the file before processing.

3. Findings (`data/findings.txt`)

  ```
  MX 1021 CONJUNCTIVA AND/OR MOUTH PALLOR
  1021 IM 2 TY 3
  ```

  where:
  ```
  MX 1021 / 1021 = Finding Number
  CONJUNCTIVA AND/OR MOUTH PALLOR = Name
  IM =   Import (1 to 5 scale)                 (*)
  TY =   Type (not used in current exercise)
  ```
