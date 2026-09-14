I: Joints forming the superior cup-like body of the animal articulating to each other.
II: Joints forming the superior cup-like body of the animal, articulating imperfectly to each other.
III: Plates forming the superior cup-like body of the animal, adhering by sutures, lined by muscular integument.
IV: The joints of the pelvis anchylose to the first columnar joint.

A: Pelvis formed of five joints (I, II, IV) / plates (III).
B: Pelvis formed of three plates (III).

_A_: Supporting five costal joints (IA) / plates (IIA, IIIA).
_B_: Five costal and one intercostal plate restng on pelvis (IIIB).
_C_: Five intercostal plates, resting on pelvis, in whose lateral angles five costal ones insert (IIIB).
_D_: Costal or intercostal plates wanting the five scapulæ, adherint to the pelvis (IIIB).

_a_: Column enlarging at the summit (IA_A_).
_b_: Column not enlarging at the summit (IA_A_, IIA_A_, IIIA_A_).

1821_miller.j.s:
  taxonomies:
  - taxon: echinodermata-order # or class?
    children:
    - taxon: crinoidea-family
      new: true
      children:
      - taxon: articulata
        children:
        - taxon: 
    - taxon: stelleridæ-family
      children:
      - taxon: comatula
      - taxon: euryale
      - taxon: ophiura
      - taxon: asteria
    - taxon: echini
    - taxon: cidares
  phylogenies:
    - treeType: diagnostic # diagnostics accumulate
      tree:
      - taxon: crinoidea
        children:
        - diagnostics:
            body: |
              Joints forming the superior cup-like body of the animal
              articulating to each other.
          taxon: articulata
          children:
          - diagnostics:
              pelvis: Formed of five joints.
            children:
            - diagnostics:
                Supporting five costal joints.
              children:
              - notes: Column enlarging at the summit.
                children:
                - notes: Fingers formed of a single series of joints.
                  taxon: apiocrinites
                  children:
                  - notes: Column round.
                    children:
                    - notes: Alimentary canal round.
                      children:
                      - notes: |
                          Articulating surface of columnar joints radiated.
                        taxon: rotundus_
                  - notes: Column eliptic.
                    children:
                    - notes: Alimentary canal round.
                      children:
                      - notes: |
                          Articulating surface of columnar joints
                          transversely-ridged. 
                        taxon: ellipticus_
              - notes: Column not enlarging at the summit.
                children:
                - notes: Fingers formed of a single series of joints.
                  children:
                  - notes: Column pentangular.
                    children:
                    - notes: Alimentary canal round.
                      children:
                      - notes: |
                          Articulating surface of columnar joints petal-shaped.
                        taxon: pentacrinites
                        children:
                        - notes: Auxiliary side arms round.
                          children:
                          - notes: In single series.
                            children:
                            - notes: Column smooth.
                              children:
                              - notes: |
                                  Columnar joints generally alternately
                                  smaller and larger.
                                taxon: Caput Medusæ_
                              - notes: |
                                  Columnar joints generally of more uniform
                                  thickness.
                                taxon: Basaltiformis_
        - taxon: semiarticulata
          notes: |
            Joints forming the superior cup-like body of the animal,
            articulating imperfectly to each other.
        - taxon: inarticulata
          notes: |
            Plates forming the superior cup-like body of the animal,
            adhering by sutures, lined by muscular integument.
        - taxon: coadunata
          notes: |
            The joints of the pelvis anchylose to the first columnar joint.
1844_buch:
  taxonomies:
  - taxon: echinodermata
    children:
    - taxon: crinoidea-family
    - taxon: cystidea-family
    new: true
