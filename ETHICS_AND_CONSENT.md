# Ethics, Consent, and Acceptable Use

This dataset contains images of **identifiable people** recorded in real university
examination halls. It was created and is released under the ethical commitments
described below. **By downloading or using any part of this dataset you agree to the
acceptable-use conditions in the final section.**

## How the data was collected

- All footage was recorded during university examination sessions at the
  International Islamic University Chittagong (IIUC), covering both real in-situ
  exams and staged scenarios.
- A single Apple iPhone 15 was mounted high on a wall or ceiling in a CCTV-like
  configuration and recorded continuous video. Footage was later compressed and
  resized to approximate standard CCTV resolution and quality.
- Data were collected from 15 classrooms, spanning a range of room sizes (roughly
  30–60 seated students per session), seating arrangements, and lighting conditions
  (bright daylight, dim daylight, and fluorescent evening sessions).

## Informed consent

- Participating students provided **informed consent** through a Google Form that
  described the study, how the data would be stored, and the process for
  withdrawal, in line with standard ethics practice for behaviour-monitoring
  research.
- The consent form explicitly asked each participant to confirm that they:
  1. voluntarily agree to be recorded (photo/video) for the research;
  2. understand the data will be used to train and test the AI monitoring
     algorithms;
  3. consent to secure storage of the data on a private drive for the duration of
     the thesis; and
  4. understand they may withdraw consent at any time before the thesis is
     finalised.
- Participants were informed about their participation, the nature of the data, and
  its intended use in this research and the associated model-building work.

## Opt-outs and removals

- **Anyone who did not consent to being recorded was excluded from the dataset, and
  any images in which they appeared were removed before this release.** The released
  data contains only frames of individuals who gave recording consent.
- The right to **withdraw** consent at any time before the thesis was finalised was
  honoured; withdrawn participants were likewise removed.
- The signed consent responses (which contain names and student IDs) are retained
  **privately by the researchers** and are **not** included in this repository or in
  the Zenodo archive, to protect participant privacy.

## Privacy safeguards

- **Raw video was never distributed.** Access to raw recordings was restricted to
  the project researchers, and the recordings were treated as private educational
  material used solely for annotation, training, and thesis defence.
- Only the released **frames and their labels** are shared. No names, roll numbers,
  or other personal identifiers are attached to any image.
- Reported results describe aggregate model performance on annotated samples and
  never identify any individual.

## Intended use and limitations

- The system built from this data is intended as **decision support for
  invigilators**, not as an automatic disciplinary or punishment tool. Any alert
  produced by a model trained on this data is meant to be verified by a human.
- Automated exam monitoring raises real concerns around privacy, fairness,
  transparency, and potential misuse. The authors do **not** present the associated
  pipeline as ready for real-world deployment. Responsible institutional use would
  require institutional clearance, clear student information, defined data-retention
  policies, secured storage, access restriction, human verification of every alert,
  and periodic fairness and reliability audits.
- All recordings come from a single institution, so cross-institution
  generalisation is not claimed.

## Acceptable-use conditions

By downloading or using this dataset, you agree that you will **not**:

1. Attempt to **re-identify**, name, contact, profile, or track any individual
   appearing in the images.
2. Use the data to **discipline, penalise, or make consequential decisions about**
   any specific person.
3. Redistribute the data in a way that strips this ethics statement or the
   attribution required by the CC BY 4.0 license.
4. Use the data for any purpose prohibited by applicable law or by the consent under
   which it was collected.

You further agree to use the data only for **research, education, and
non-harmful development**, and to honour any reasonable data-removal request.

## Data-removal requests

If you are a participant (or their representative) and would like content removed,
or if you have any ethical concern about this release, please open an issue or
contact the authors listed in [`README.md`](README.md). Reasonable requests will be
honoured promptly.
