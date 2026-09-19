# Benchmark V2 Gold Annotation Candidates

Benchmark version: 2.0
Corpus SHA-256: 16c01b5dfb1753d0b55dafdf6164d977383c0419c4ebfe8b376189aaf7ef9e62
Queries: 32

Relevance scale:
- 3 = directly answer-bearing
- 2 = strongly supporting
- 1 = weak/supporting
- blank = irrelevant or not yet annotated

---

## Q001

**Query:** What does ef_construct control?

**Query class:** exact+semantic

**Answerability:** answerable

### Document DOC-002

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-002::P000::HNSW Construction and ef_construct::904ce0a9d704`

**section_path:** HNSW Construction and ef_construct

**Parent relevance:** `[   ]`

Document ID: DOC-002

##### Child 0

**child_key:** `DOC-002::P000::HNSW Construction and ef_construct::904ce0a9d704::C000::904ce0a9d704`

**Child relevance:** `[   ]`

Document ID: DOC-002

#### Parent 1

**parent_key:** `DOC-002::P001::HNSW Construction and ef_construct/Meaning::773bd0415a3a`

**section_path:** HNSW Construction and ef_construct > Meaning

**Parent relevance:** `[   ]`

ef_construct controls how broadly HNSW explores candidate neighbors while inserting vectors during index construction. Larger values let the builder consider more alternatives and can produce a higher-quality graph.

##### Child 0

**child_key:** `DOC-002::P001::HNSW Construction and ef_construct/Meaning::773bd0415a3a::C000::f829297fe9a8`

**Child relevance:** `[   ]`

ef_construct controls how broadly HNSW explores candidate neighbors while inserting vectors during index construction.

##### Child 1

**child_key:** `DOC-002::P001::HNSW Construction and ef_construct/Meaning::773bd0415a3a::C001::409b5fac7b8f`

**Child relevance:** `[   ]`

during index construction. Larger values let the builder consider more alternatives and can produce a higher-quality

##### Child 2

**child_key:** `DOC-002::P001::HNSW Construction and ef_construct/Meaning::773bd0415a3a::C002::e63d79f02c32`

**Child relevance:** `[   ]`

can produce a higher-quality graph.

#### Parent 2

**parent_key:** `DOC-002::P002::HNSW Construction and ef_construct/Trade-off::b45d541354d0`

**section_path:** HNSW Construction and ef_construct > Trade-off

**Parent relevance:** `[   ]`

Higher ef_construct increases index-build time. Better graph quality may improve recall later, but it does not guarantee that every query becomes faster. Dataset size, distribution, dimensionality, M, and ef_search all interact.

##### Child 0

**child_key:** `DOC-002::P002::HNSW Construction and ef_construct/Trade-off::b45d541354d0::C000::7601bd262c82`

**Child relevance:** `[   ]`

Higher ef_construct increases index-build time. Better graph quality may improve recall later, but it does not

##### Child 1

**child_key:** `DOC-002::P002::HNSW Construction and ef_construct/Trade-off::b45d541354d0::C001::228c23614660`

**Child relevance:** `[   ]`

recall later, but it does not guarantee that every query becomes faster. Dataset size, distribution, dimensionality, M,

##### Child 2

**child_key:** `DOC-002::P002::HNSW Construction and ef_construct/Trade-off::b45d541354d0::C002::334763e5634e`

**Child relevance:** `[   ]`

dimensionality, M, and ef_search all interact.

#### Parent 3

**parent_key:** `DOC-002::P003::HNSW Construction and ef_construct/Example::2778af8c24c5`

**section_path:** HNSW Construction and ef_construct > Example

**Parent relevance:** `[   ]`

With M=16 and ef_construct=100, sixteen describes the graph connectivity target while one hundred describes construction-time candidate breadth. ef_construct=100 does not mean one hundred layers or one hundred edges.

##### Child 0

**child_key:** `DOC-002::P003::HNSW Construction and ef_construct/Example::2778af8c24c5::C000::0b16b3f7b7d1`

**Child relevance:** `[   ]`

With M=16 and ef_construct=100, sixteen describes the graph connectivity target while one hundred describes

##### Child 1

**child_key:** `DOC-002::P003::HNSW Construction and ef_construct/Example::2778af8c24c5::C001::09a4a84e762a`

**Child relevance:** `[   ]`

while one hundred describes construction-time candidate breadth. ef_construct=100 does not mean one hundred layers or

##### Child 2

**child_key:** `DOC-002::P003::HNSW Construction and ef_construct/Example::2778af8c24c5::C002::86c1f3b6844c`

**Child relevance:** `[   ]`

not mean one hundred layers or one hundred edges.

#### Parent 4

**parent_key:** `DOC-002::P004::HNSW Construction and ef_construct/Rebuild::733c8f222879`

**section_path:** HNSW Construction and ef_construct > Rebuild

**Parent relevance:** `[   ]`

Changing ef_construct affects index construction, so an existing HNSW graph generally needs rebuilding before the change can influence graph quality.

##### Child 0

**child_key:** `DOC-002::P004::HNSW Construction and ef_construct/Rebuild::733c8f222879::C000::960357e05e70`

**Child relevance:** `[   ]`

Changing ef_construct affects index construction, so an existing HNSW graph generally needs rebuilding before the

##### Child 1

**child_key:** `DOC-002::P004::HNSW Construction and ef_construct/Rebuild::733c8f222879::C001::90e54da7f64b`

**Child relevance:** `[   ]`

needs rebuilding before the change can influence graph quality.

---

## Q002

**Query:** How can I improve graph quality during index construction?

**Query class:** semantic paraphrase

**Answerability:** answerable

### Document DOC-002

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-002::P000::HNSW Construction and ef_construct::904ce0a9d704`

**section_path:** HNSW Construction and ef_construct

**Parent relevance:** `[   ]`

Document ID: DOC-002

##### Child 0

**child_key:** `DOC-002::P000::HNSW Construction and ef_construct::904ce0a9d704::C000::904ce0a9d704`

**Child relevance:** `[   ]`

Document ID: DOC-002

#### Parent 1

**parent_key:** `DOC-002::P001::HNSW Construction and ef_construct/Meaning::773bd0415a3a`

**section_path:** HNSW Construction and ef_construct > Meaning

**Parent relevance:** `[   ]`

ef_construct controls how broadly HNSW explores candidate neighbors while inserting vectors during index construction. Larger values let the builder consider more alternatives and can produce a higher-quality graph.

##### Child 0

**child_key:** `DOC-002::P001::HNSW Construction and ef_construct/Meaning::773bd0415a3a::C000::f829297fe9a8`

**Child relevance:** `[   ]`

ef_construct controls how broadly HNSW explores candidate neighbors while inserting vectors during index construction.

##### Child 1

**child_key:** `DOC-002::P001::HNSW Construction and ef_construct/Meaning::773bd0415a3a::C001::409b5fac7b8f`

**Child relevance:** `[   ]`

during index construction. Larger values let the builder consider more alternatives and can produce a higher-quality

##### Child 2

**child_key:** `DOC-002::P001::HNSW Construction and ef_construct/Meaning::773bd0415a3a::C002::e63d79f02c32`

**Child relevance:** `[   ]`

can produce a higher-quality graph.

#### Parent 2

**parent_key:** `DOC-002::P002::HNSW Construction and ef_construct/Trade-off::b45d541354d0`

**section_path:** HNSW Construction and ef_construct > Trade-off

**Parent relevance:** `[   ]`

Higher ef_construct increases index-build time. Better graph quality may improve recall later, but it does not guarantee that every query becomes faster. Dataset size, distribution, dimensionality, M, and ef_search all interact.

##### Child 0

**child_key:** `DOC-002::P002::HNSW Construction and ef_construct/Trade-off::b45d541354d0::C000::7601bd262c82`

**Child relevance:** `[   ]`

Higher ef_construct increases index-build time. Better graph quality may improve recall later, but it does not

##### Child 1

**child_key:** `DOC-002::P002::HNSW Construction and ef_construct/Trade-off::b45d541354d0::C001::228c23614660`

**Child relevance:** `[   ]`

recall later, but it does not guarantee that every query becomes faster. Dataset size, distribution, dimensionality, M,

##### Child 2

**child_key:** `DOC-002::P002::HNSW Construction and ef_construct/Trade-off::b45d541354d0::C002::334763e5634e`

**Child relevance:** `[   ]`

dimensionality, M, and ef_search all interact.

#### Parent 3

**parent_key:** `DOC-002::P003::HNSW Construction and ef_construct/Example::2778af8c24c5`

**section_path:** HNSW Construction and ef_construct > Example

**Parent relevance:** `[   ]`

With M=16 and ef_construct=100, sixteen describes the graph connectivity target while one hundred describes construction-time candidate breadth. ef_construct=100 does not mean one hundred layers or one hundred edges.

##### Child 0

**child_key:** `DOC-002::P003::HNSW Construction and ef_construct/Example::2778af8c24c5::C000::0b16b3f7b7d1`

**Child relevance:** `[   ]`

With M=16 and ef_construct=100, sixteen describes the graph connectivity target while one hundred describes

##### Child 1

**child_key:** `DOC-002::P003::HNSW Construction and ef_construct/Example::2778af8c24c5::C001::09a4a84e762a`

**Child relevance:** `[   ]`

while one hundred describes construction-time candidate breadth. ef_construct=100 does not mean one hundred layers or

##### Child 2

**child_key:** `DOC-002::P003::HNSW Construction and ef_construct/Example::2778af8c24c5::C002::86c1f3b6844c`

**Child relevance:** `[   ]`

not mean one hundred layers or one hundred edges.

#### Parent 4

**parent_key:** `DOC-002::P004::HNSW Construction and ef_construct/Rebuild::733c8f222879`

**section_path:** HNSW Construction and ef_construct > Rebuild

**Parent relevance:** `[   ]`

Changing ef_construct affects index construction, so an existing HNSW graph generally needs rebuilding before the change can influence graph quality.

##### Child 0

**child_key:** `DOC-002::P004::HNSW Construction and ef_construct/Rebuild::733c8f222879::C000::960357e05e70`

**Child relevance:** `[   ]`

Changing ef_construct affects index construction, so an existing HNSW graph generally needs rebuilding before the

##### Child 1

**child_key:** `DOC-002::P004::HNSW Construction and ef_construct/Rebuild::733c8f222879::C001::90e54da7f64b`

**Child relevance:** `[   ]`

needs rebuilding before the change can influence graph quality.

---

## Q003

**Query:** Does ef_construct determine the number of HNSW layers?

**Query class:** concept discrimination

**Answerability:** answerable

### Document DOC-002

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-002::P000::HNSW Construction and ef_construct::904ce0a9d704`

**section_path:** HNSW Construction and ef_construct

**Parent relevance:** `[   ]`

Document ID: DOC-002

##### Child 0

**child_key:** `DOC-002::P000::HNSW Construction and ef_construct::904ce0a9d704::C000::904ce0a9d704`

**Child relevance:** `[   ]`

Document ID: DOC-002

#### Parent 1

**parent_key:** `DOC-002::P001::HNSW Construction and ef_construct/Meaning::773bd0415a3a`

**section_path:** HNSW Construction and ef_construct > Meaning

**Parent relevance:** `[   ]`

ef_construct controls how broadly HNSW explores candidate neighbors while inserting vectors during index construction. Larger values let the builder consider more alternatives and can produce a higher-quality graph.

##### Child 0

**child_key:** `DOC-002::P001::HNSW Construction and ef_construct/Meaning::773bd0415a3a::C000::f829297fe9a8`

**Child relevance:** `[   ]`

ef_construct controls how broadly HNSW explores candidate neighbors while inserting vectors during index construction.

##### Child 1

**child_key:** `DOC-002::P001::HNSW Construction and ef_construct/Meaning::773bd0415a3a::C001::409b5fac7b8f`

**Child relevance:** `[   ]`

during index construction. Larger values let the builder consider more alternatives and can produce a higher-quality

##### Child 2

**child_key:** `DOC-002::P001::HNSW Construction and ef_construct/Meaning::773bd0415a3a::C002::e63d79f02c32`

**Child relevance:** `[   ]`

can produce a higher-quality graph.

#### Parent 2

**parent_key:** `DOC-002::P002::HNSW Construction and ef_construct/Trade-off::b45d541354d0`

**section_path:** HNSW Construction and ef_construct > Trade-off

**Parent relevance:** `[   ]`

Higher ef_construct increases index-build time. Better graph quality may improve recall later, but it does not guarantee that every query becomes faster. Dataset size, distribution, dimensionality, M, and ef_search all interact.

##### Child 0

**child_key:** `DOC-002::P002::HNSW Construction and ef_construct/Trade-off::b45d541354d0::C000::7601bd262c82`

**Child relevance:** `[   ]`

Higher ef_construct increases index-build time. Better graph quality may improve recall later, but it does not

##### Child 1

**child_key:** `DOC-002::P002::HNSW Construction and ef_construct/Trade-off::b45d541354d0::C001::228c23614660`

**Child relevance:** `[   ]`

recall later, but it does not guarantee that every query becomes faster. Dataset size, distribution, dimensionality, M,

##### Child 2

**child_key:** `DOC-002::P002::HNSW Construction and ef_construct/Trade-off::b45d541354d0::C002::334763e5634e`

**Child relevance:** `[   ]`

dimensionality, M, and ef_search all interact.

#### Parent 3

**parent_key:** `DOC-002::P003::HNSW Construction and ef_construct/Example::2778af8c24c5`

**section_path:** HNSW Construction and ef_construct > Example

**Parent relevance:** `[   ]`

With M=16 and ef_construct=100, sixteen describes the graph connectivity target while one hundred describes construction-time candidate breadth. ef_construct=100 does not mean one hundred layers or one hundred edges.

##### Child 0

**child_key:** `DOC-002::P003::HNSW Construction and ef_construct/Example::2778af8c24c5::C000::0b16b3f7b7d1`

**Child relevance:** `[   ]`

With M=16 and ef_construct=100, sixteen describes the graph connectivity target while one hundred describes

##### Child 1

**child_key:** `DOC-002::P003::HNSW Construction and ef_construct/Example::2778af8c24c5::C001::09a4a84e762a`

**Child relevance:** `[   ]`

while one hundred describes construction-time candidate breadth. ef_construct=100 does not mean one hundred layers or

##### Child 2

**child_key:** `DOC-002::P003::HNSW Construction and ef_construct/Example::2778af8c24c5::C002::86c1f3b6844c`

**Child relevance:** `[   ]`

not mean one hundred layers or one hundred edges.

#### Parent 4

**parent_key:** `DOC-002::P004::HNSW Construction and ef_construct/Rebuild::733c8f222879`

**section_path:** HNSW Construction and ef_construct > Rebuild

**Parent relevance:** `[   ]`

Changing ef_construct affects index construction, so an existing HNSW graph generally needs rebuilding before the change can influence graph quality.

##### Child 0

**child_key:** `DOC-002::P004::HNSW Construction and ef_construct/Rebuild::733c8f222879::C000::960357e05e70`

**Child relevance:** `[   ]`

Changing ef_construct affects index construction, so an existing HNSW graph generally needs rebuilding before the

##### Child 1

**child_key:** `DOC-002::P004::HNSW Construction and ef_construct/Rebuild::733c8f222879::C001::90e54da7f64b`

**Child relevance:** `[   ]`

needs rebuilding before the change can influence graph quality.

### Document DOC-001

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-001::P000::HNSW Architecture and Search::17c49e1f6340`

**section_path:** HNSW Architecture and Search

**Parent relevance:** `[   ]`

Document ID: DOC-001

##### Child 0

**child_key:** `DOC-001::P000::HNSW Architecture and Search::17c49e1f6340::C000::17c49e1f6340`

**Child relevance:** `[   ]`

Document ID: DOC-001

#### Parent 1

**parent_key:** `DOC-001::P001::HNSW Architecture and Search/Layers::b55e6422027d`

**section_path:** HNSW Architecture and Search > Layers

**Parent relevance:** `[   ]`

HNSW organizes vectors in hierarchical proximity graphs. Upper layers are sparse and support long-range routing; lower layers contain denser local neighborhoods. Search begins high in the hierarchy and descends while moving toward better candidates. This allows approximate nearest-neighbor search without comparing the query against every stored vector.

##### Child 0

**child_key:** `DOC-001::P001::HNSW Architecture and Search/Layers::b55e6422027d::C000::b0dcbbe05fcc`

**Child relevance:** `[   ]`

HNSW organizes vectors in hierarchical proximity graphs. Upper layers are sparse and support long-range routing; lower

##### Child 1

**child_key:** `DOC-001::P001::HNSW Architecture and Search/Layers::b55e6422027d::C001::584ff998efd3`

**Child relevance:** `[   ]`

long-range routing; lower layers contain denser local neighborhoods. Search begins high in the hierarchy and descends

##### Child 2

**child_key:** `DOC-001::P001::HNSW Architecture and Search/Layers::b55e6422027d::C002::8ac6f406be0c`

**Child relevance:** `[   ]`

in the hierarchy and descends while moving toward better candidates. This allows approximate nearest-neighbor search

##### Child 3

**child_key:** `DOC-001::P001::HNSW Architecture and Search/Layers::b55e6422027d::C003::1e6e3c76945b`

**Child relevance:** `[   ]`

nearest-neighbor search without comparing the query against every stored vector.

#### Parent 2

**parent_key:** `DOC-001::P002::HNSW Architecture and Search/M parameter::b61b6a7550b4`

**section_path:** HNSW Architecture and Search > M parameter

**Parent relevance:** `[   ]`

M controls the target graph connectivity per node. Larger M usually improves navigation and recall, especially on clustered data, but increases memory consumption and construction cost. M is not the number of hierarchy layers.

##### Child 0

**child_key:** `DOC-001::P002::HNSW Architecture and Search/M parameter::b61b6a7550b4::C000::57a20429d6b5`

**Child relevance:** `[   ]`

M controls the target graph connectivity per node. Larger M usually improves navigation and recall, especially on

##### Child 1

**child_key:** `DOC-001::P002::HNSW Architecture and Search/M parameter::b61b6a7550b4::C001::1fe6b7cc9b71`

**Child relevance:** `[   ]`

and recall, especially on clustered data, but increases memory consumption and construction cost. M is not the number

##### Child 2

**child_key:** `DOC-001::P002::HNSW Architecture and Search/M parameter::b61b6a7550b4::C002::9b31f6cbd874`

**Child relevance:** `[   ]`

cost. M is not the number of hierarchy layers.

#### Parent 3

**parent_key:** `DOC-001::P003::HNSW Architecture and Search/ef_search::f62895d48bb3`

**section_path:** HNSW Architecture and Search > ef_search

**Parent relevance:** `[   ]`

ef_search controls query-time search breadth. Larger values keep more candidates in the search frontier and usually improve recall at the cost of latency. It is not a count of graph edges.

##### Child 0

**child_key:** `DOC-001::P003::HNSW Architecture and Search/ef_search::f62895d48bb3::C000::19774f23ec94`

**Child relevance:** `[   ]`

ef_search controls query-time search breadth. Larger values keep more candidates in the search frontier and usually

##### Child 1

**child_key:** `DOC-001::P003::HNSW Architecture and Search/ef_search::f62895d48bb3::C001::8ec2c9cb3881`

**Child relevance:** `[   ]`

search frontier and usually improve recall at the cost of latency. It is not a count of graph edges.

#### Parent 4

**parent_key:** `DOC-001::P004::HNSW Architecture and Search/Tuning::2f9d5b9109dc`

**section_path:** HNSW Architecture and Search > Tuning

**Parent relevance:** `[   ]`

Tune recall and latency together. M is primarily an index-structure choice while ef_search can often be adjusted per query or workload.

##### Child 0

**child_key:** `DOC-001::P004::HNSW Architecture and Search/Tuning::2f9d5b9109dc::C000::cf42e756f571`

**Child relevance:** `[   ]`

Tune recall and latency together. M is primarily an index-structure choice while ef_search can often be adjusted per

##### Child 1

**child_key:** `DOC-001::P004::HNSW Architecture and Search/Tuning::2f9d5b9109dc::C001::697d4b5a6090`

**Child relevance:** `[   ]`

can often be adjusted per query or workload.

---

## Q004

**Query:** What does the M parameter change in HNSW?

**Query class:** exact technical

**Answerability:** answerable

### Document DOC-001

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-001::P000::HNSW Architecture and Search::17c49e1f6340`

**section_path:** HNSW Architecture and Search

**Parent relevance:** `[   ]`

Document ID: DOC-001

##### Child 0

**child_key:** `DOC-001::P000::HNSW Architecture and Search::17c49e1f6340::C000::17c49e1f6340`

**Child relevance:** `[   ]`

Document ID: DOC-001

#### Parent 1

**parent_key:** `DOC-001::P001::HNSW Architecture and Search/Layers::b55e6422027d`

**section_path:** HNSW Architecture and Search > Layers

**Parent relevance:** `[   ]`

HNSW organizes vectors in hierarchical proximity graphs. Upper layers are sparse and support long-range routing; lower layers contain denser local neighborhoods. Search begins high in the hierarchy and descends while moving toward better candidates. This allows approximate nearest-neighbor search without comparing the query against every stored vector.

##### Child 0

**child_key:** `DOC-001::P001::HNSW Architecture and Search/Layers::b55e6422027d::C000::b0dcbbe05fcc`

**Child relevance:** `[   ]`

HNSW organizes vectors in hierarchical proximity graphs. Upper layers are sparse and support long-range routing; lower

##### Child 1

**child_key:** `DOC-001::P001::HNSW Architecture and Search/Layers::b55e6422027d::C001::584ff998efd3`

**Child relevance:** `[   ]`

long-range routing; lower layers contain denser local neighborhoods. Search begins high in the hierarchy and descends

##### Child 2

**child_key:** `DOC-001::P001::HNSW Architecture and Search/Layers::b55e6422027d::C002::8ac6f406be0c`

**Child relevance:** `[   ]`

in the hierarchy and descends while moving toward better candidates. This allows approximate nearest-neighbor search

##### Child 3

**child_key:** `DOC-001::P001::HNSW Architecture and Search/Layers::b55e6422027d::C003::1e6e3c76945b`

**Child relevance:** `[   ]`

nearest-neighbor search without comparing the query against every stored vector.

#### Parent 2

**parent_key:** `DOC-001::P002::HNSW Architecture and Search/M parameter::b61b6a7550b4`

**section_path:** HNSW Architecture and Search > M parameter

**Parent relevance:** `[   ]`

M controls the target graph connectivity per node. Larger M usually improves navigation and recall, especially on clustered data, but increases memory consumption and construction cost. M is not the number of hierarchy layers.

##### Child 0

**child_key:** `DOC-001::P002::HNSW Architecture and Search/M parameter::b61b6a7550b4::C000::57a20429d6b5`

**Child relevance:** `[   ]`

M controls the target graph connectivity per node. Larger M usually improves navigation and recall, especially on

##### Child 1

**child_key:** `DOC-001::P002::HNSW Architecture and Search/M parameter::b61b6a7550b4::C001::1fe6b7cc9b71`

**Child relevance:** `[   ]`

and recall, especially on clustered data, but increases memory consumption and construction cost. M is not the number

##### Child 2

**child_key:** `DOC-001::P002::HNSW Architecture and Search/M parameter::b61b6a7550b4::C002::9b31f6cbd874`

**Child relevance:** `[   ]`

cost. M is not the number of hierarchy layers.

#### Parent 3

**parent_key:** `DOC-001::P003::HNSW Architecture and Search/ef_search::f62895d48bb3`

**section_path:** HNSW Architecture and Search > ef_search

**Parent relevance:** `[   ]`

ef_search controls query-time search breadth. Larger values keep more candidates in the search frontier and usually improve recall at the cost of latency. It is not a count of graph edges.

##### Child 0

**child_key:** `DOC-001::P003::HNSW Architecture and Search/ef_search::f62895d48bb3::C000::19774f23ec94`

**Child relevance:** `[   ]`

ef_search controls query-time search breadth. Larger values keep more candidates in the search frontier and usually

##### Child 1

**child_key:** `DOC-001::P003::HNSW Architecture and Search/ef_search::f62895d48bb3::C001::8ec2c9cb3881`

**Child relevance:** `[   ]`

search frontier and usually improve recall at the cost of latency. It is not a count of graph edges.

#### Parent 4

**parent_key:** `DOC-001::P004::HNSW Architecture and Search/Tuning::2f9d5b9109dc`

**section_path:** HNSW Architecture and Search > Tuning

**Parent relevance:** `[   ]`

Tune recall and latency together. M is primarily an index-structure choice while ef_search can often be adjusted per query or workload.

##### Child 0

**child_key:** `DOC-001::P004::HNSW Architecture and Search/Tuning::2f9d5b9109dc::C000::cf42e756f571`

**Child relevance:** `[   ]`

Tune recall and latency together. M is primarily an index-structure choice while ef_search can often be adjusted per

##### Child 1

**child_key:** `DOC-001::P004::HNSW Architecture and Search/Tuning::2f9d5b9109dc::C001::697d4b5a6090`

**Child relevance:** `[   ]`

can often be adjusted per query or workload.

---

## Q005

**Query:** How does HNSW avoid comparing every vector?

**Query class:** semantic

**Answerability:** answerable

### Document DOC-001

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-001::P000::HNSW Architecture and Search::17c49e1f6340`

**section_path:** HNSW Architecture and Search

**Parent relevance:** `[   ]`

Document ID: DOC-001

##### Child 0

**child_key:** `DOC-001::P000::HNSW Architecture and Search::17c49e1f6340::C000::17c49e1f6340`

**Child relevance:** `[   ]`

Document ID: DOC-001

#### Parent 1

**parent_key:** `DOC-001::P001::HNSW Architecture and Search/Layers::b55e6422027d`

**section_path:** HNSW Architecture and Search > Layers

**Parent relevance:** `[   ]`

HNSW organizes vectors in hierarchical proximity graphs. Upper layers are sparse and support long-range routing; lower layers contain denser local neighborhoods. Search begins high in the hierarchy and descends while moving toward better candidates. This allows approximate nearest-neighbor search without comparing the query against every stored vector.

##### Child 0

**child_key:** `DOC-001::P001::HNSW Architecture and Search/Layers::b55e6422027d::C000::b0dcbbe05fcc`

**Child relevance:** `[   ]`

HNSW organizes vectors in hierarchical proximity graphs. Upper layers are sparse and support long-range routing; lower

##### Child 1

**child_key:** `DOC-001::P001::HNSW Architecture and Search/Layers::b55e6422027d::C001::584ff998efd3`

**Child relevance:** `[   ]`

long-range routing; lower layers contain denser local neighborhoods. Search begins high in the hierarchy and descends

##### Child 2

**child_key:** `DOC-001::P001::HNSW Architecture and Search/Layers::b55e6422027d::C002::8ac6f406be0c`

**Child relevance:** `[   ]`

in the hierarchy and descends while moving toward better candidates. This allows approximate nearest-neighbor search

##### Child 3

**child_key:** `DOC-001::P001::HNSW Architecture and Search/Layers::b55e6422027d::C003::1e6e3c76945b`

**Child relevance:** `[   ]`

nearest-neighbor search without comparing the query against every stored vector.

#### Parent 2

**parent_key:** `DOC-001::P002::HNSW Architecture and Search/M parameter::b61b6a7550b4`

**section_path:** HNSW Architecture and Search > M parameter

**Parent relevance:** `[   ]`

M controls the target graph connectivity per node. Larger M usually improves navigation and recall, especially on clustered data, but increases memory consumption and construction cost. M is not the number of hierarchy layers.

##### Child 0

**child_key:** `DOC-001::P002::HNSW Architecture and Search/M parameter::b61b6a7550b4::C000::57a20429d6b5`

**Child relevance:** `[   ]`

M controls the target graph connectivity per node. Larger M usually improves navigation and recall, especially on

##### Child 1

**child_key:** `DOC-001::P002::HNSW Architecture and Search/M parameter::b61b6a7550b4::C001::1fe6b7cc9b71`

**Child relevance:** `[   ]`

and recall, especially on clustered data, but increases memory consumption and construction cost. M is not the number

##### Child 2

**child_key:** `DOC-001::P002::HNSW Architecture and Search/M parameter::b61b6a7550b4::C002::9b31f6cbd874`

**Child relevance:** `[   ]`

cost. M is not the number of hierarchy layers.

#### Parent 3

**parent_key:** `DOC-001::P003::HNSW Architecture and Search/ef_search::f62895d48bb3`

**section_path:** HNSW Architecture and Search > ef_search

**Parent relevance:** `[   ]`

ef_search controls query-time search breadth. Larger values keep more candidates in the search frontier and usually improve recall at the cost of latency. It is not a count of graph edges.

##### Child 0

**child_key:** `DOC-001::P003::HNSW Architecture and Search/ef_search::f62895d48bb3::C000::19774f23ec94`

**Child relevance:** `[   ]`

ef_search controls query-time search breadth. Larger values keep more candidates in the search frontier and usually

##### Child 1

**child_key:** `DOC-001::P003::HNSW Architecture and Search/ef_search::f62895d48bb3::C001::8ec2c9cb3881`

**Child relevance:** `[   ]`

search frontier and usually improve recall at the cost of latency. It is not a count of graph edges.

#### Parent 4

**parent_key:** `DOC-001::P004::HNSW Architecture and Search/Tuning::2f9d5b9109dc`

**section_path:** HNSW Architecture and Search > Tuning

**Parent relevance:** `[   ]`

Tune recall and latency together. M is primarily an index-structure choice while ef_search can often be adjusted per query or workload.

##### Child 0

**child_key:** `DOC-001::P004::HNSW Architecture and Search/Tuning::2f9d5b9109dc::C000::cf42e756f571`

**Child relevance:** `[   ]`

Tune recall and latency together. M is primarily an index-structure choice while ef_search can often be adjusted per

##### Child 1

**child_key:** `DOC-001::P004::HNSW Architecture and Search/Tuning::2f9d5b9109dc::C001::697d4b5a6090`

**Child relevance:** `[   ]`

can often be adjusted per query or workload.

---

## Q006

**Query:** What is ef_search used for?

**Query class:** exact technical

**Answerability:** answerable

### Document DOC-001

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-001::P000::HNSW Architecture and Search::17c49e1f6340`

**section_path:** HNSW Architecture and Search

**Parent relevance:** `[   ]`

Document ID: DOC-001

##### Child 0

**child_key:** `DOC-001::P000::HNSW Architecture and Search::17c49e1f6340::C000::17c49e1f6340`

**Child relevance:** `[   ]`

Document ID: DOC-001

#### Parent 1

**parent_key:** `DOC-001::P001::HNSW Architecture and Search/Layers::b55e6422027d`

**section_path:** HNSW Architecture and Search > Layers

**Parent relevance:** `[   ]`

HNSW organizes vectors in hierarchical proximity graphs. Upper layers are sparse and support long-range routing; lower layers contain denser local neighborhoods. Search begins high in the hierarchy and descends while moving toward better candidates. This allows approximate nearest-neighbor search without comparing the query against every stored vector.

##### Child 0

**child_key:** `DOC-001::P001::HNSW Architecture and Search/Layers::b55e6422027d::C000::b0dcbbe05fcc`

**Child relevance:** `[   ]`

HNSW organizes vectors in hierarchical proximity graphs. Upper layers are sparse and support long-range routing; lower

##### Child 1

**child_key:** `DOC-001::P001::HNSW Architecture and Search/Layers::b55e6422027d::C001::584ff998efd3`

**Child relevance:** `[   ]`

long-range routing; lower layers contain denser local neighborhoods. Search begins high in the hierarchy and descends

##### Child 2

**child_key:** `DOC-001::P001::HNSW Architecture and Search/Layers::b55e6422027d::C002::8ac6f406be0c`

**Child relevance:** `[   ]`

in the hierarchy and descends while moving toward better candidates. This allows approximate nearest-neighbor search

##### Child 3

**child_key:** `DOC-001::P001::HNSW Architecture and Search/Layers::b55e6422027d::C003::1e6e3c76945b`

**Child relevance:** `[   ]`

nearest-neighbor search without comparing the query against every stored vector.

#### Parent 2

**parent_key:** `DOC-001::P002::HNSW Architecture and Search/M parameter::b61b6a7550b4`

**section_path:** HNSW Architecture and Search > M parameter

**Parent relevance:** `[   ]`

M controls the target graph connectivity per node. Larger M usually improves navigation and recall, especially on clustered data, but increases memory consumption and construction cost. M is not the number of hierarchy layers.

##### Child 0

**child_key:** `DOC-001::P002::HNSW Architecture and Search/M parameter::b61b6a7550b4::C000::57a20429d6b5`

**Child relevance:** `[   ]`

M controls the target graph connectivity per node. Larger M usually improves navigation and recall, especially on

##### Child 1

**child_key:** `DOC-001::P002::HNSW Architecture and Search/M parameter::b61b6a7550b4::C001::1fe6b7cc9b71`

**Child relevance:** `[   ]`

and recall, especially on clustered data, but increases memory consumption and construction cost. M is not the number

##### Child 2

**child_key:** `DOC-001::P002::HNSW Architecture and Search/M parameter::b61b6a7550b4::C002::9b31f6cbd874`

**Child relevance:** `[   ]`

cost. M is not the number of hierarchy layers.

#### Parent 3

**parent_key:** `DOC-001::P003::HNSW Architecture and Search/ef_search::f62895d48bb3`

**section_path:** HNSW Architecture and Search > ef_search

**Parent relevance:** `[   ]`

ef_search controls query-time search breadth. Larger values keep more candidates in the search frontier and usually improve recall at the cost of latency. It is not a count of graph edges.

##### Child 0

**child_key:** `DOC-001::P003::HNSW Architecture and Search/ef_search::f62895d48bb3::C000::19774f23ec94`

**Child relevance:** `[   ]`

ef_search controls query-time search breadth. Larger values keep more candidates in the search frontier and usually

##### Child 1

**child_key:** `DOC-001::P003::HNSW Architecture and Search/ef_search::f62895d48bb3::C001::8ec2c9cb3881`

**Child relevance:** `[   ]`

search frontier and usually improve recall at the cost of latency. It is not a count of graph edges.

#### Parent 4

**parent_key:** `DOC-001::P004::HNSW Architecture and Search/Tuning::2f9d5b9109dc`

**section_path:** HNSW Architecture and Search > Tuning

**Parent relevance:** `[   ]`

Tune recall and latency together. M is primarily an index-structure choice while ef_search can often be adjusted per query or workload.

##### Child 0

**child_key:** `DOC-001::P004::HNSW Architecture and Search/Tuning::2f9d5b9109dc::C000::cf42e756f571`

**Child relevance:** `[   ]`

Tune recall and latency together. M is primarily an index-structure choice while ef_search can often be adjusted per

##### Child 1

**child_key:** `DOC-001::P004::HNSW Architecture and Search/Tuning::2f9d5b9109dc::C001::697d4b5a6090`

**Child relevance:** `[   ]`

can often be adjusted per query or workload.

---

## Q007

**Query:** Why might BM25 beat embeddings for uq_document_content_hash?

**Query class:** identifier

**Answerability:** answerable

### Document DOC-004

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-004::P000::Sparse Retrieval and BM25::2e408419645d`

**section_path:** Sparse Retrieval and BM25

**Parent relevance:** `[   ]`

Document ID: DOC-004

##### Child 0

**child_key:** `DOC-004::P000::Sparse Retrieval and BM25::2e408419645d::C000::2e408419645d`

**Child relevance:** `[   ]`

Document ID: DOC-004

#### Parent 1

**parent_key:** `DOC-004::P001::Sparse Retrieval and BM25/Lexical::85dbef0962d2`

**section_path:** Sparse Retrieval and BM25 > Lexical

**Parent relevance:** `[   ]`

BM25 uses explicit lexical evidence and rewards informative term matches while accounting for collection frequency and document length.

##### Child 0

**child_key:** `DOC-004::P001::Sparse Retrieval and BM25/Lexical::85dbef0962d2::C000::4be0fb0dd5f2`

**Child relevance:** `[   ]`

BM25 uses explicit lexical evidence and rewards informative term matches while accounting for collection frequency and

##### Child 1

**child_key:** `DOC-004::P001::Sparse Retrieval and BM25/Lexical::85dbef0962d2::C001::8451d40249b1`

**Child relevance:** `[   ]`

for collection frequency and document length.

#### Parent 2

**parent_key:** `DOC-004::P002::Sparse Retrieval and BM25/Identifiers::591b164e8bfc`

**section_path:** Sparse Retrieval and BM25 > Identifiers

**Parent relevance:** `[   ]`

Exact terms such as ef_construct, HTTP 422, tenant_id, vector_size, and uq_document_content_hash are strong sparse-search signals.

##### Child 0

**child_key:** `DOC-004::P002::Sparse Retrieval and BM25/Identifiers::591b164e8bfc::C000::7b2b4c61478c`

**Child relevance:** `[   ]`

Exact terms such as ef_construct, HTTP 422, tenant_id, vector_size, and uq_document_content_hash are strong

##### Child 1

**child_key:** `DOC-004::P002::Sparse Retrieval and BM25/Identifiers::591b164e8bfc::C001::359bc6fc3d42`

**Child relevance:** `[   ]`

are strong sparse-search signals.

#### Parent 3

**parent_key:** `DOC-004::P003::Sparse Retrieval and BM25/Limit::2667a2c792be`

**section_path:** Sparse Retrieval and BM25 > Limit

**Parent relevance:** `[   ]`

Sparse retrieval does not generalize paraphrases like a dense model. Build phase and index construction may refer to the same concept without sharing the same terms.

##### Child 0

**child_key:** `DOC-004::P003::Sparse Retrieval and BM25/Limit::2667a2c792be::C000::e4a57921ae4e`

**Child relevance:** `[   ]`

Sparse retrieval does not generalize paraphrases like a dense model. Build phase and index construction may refer to

##### Child 1

**child_key:** `DOC-004::P003::Sparse Retrieval and BM25/Limit::2667a2c792be::C001::d1d1320a8897`

**Child relevance:** `[   ]`

construction may refer to the same concept without sharing the same terms.

#### Parent 4

**parent_key:** `DOC-004::P004::Sparse Retrieval and BM25/Role::f68b5454a7a0`

**section_path:** Sparse Retrieval and BM25 > Role

**Parent relevance:** `[   ]`

Dense and sparse retrieval are complementary: dense adds semantic generalization and sparse adds exact lexical precision.

##### Child 0

**child_key:** `DOC-004::P004::Sparse Retrieval and BM25/Role::f68b5454a7a0::C000::d8c291559660`

**Child relevance:** `[   ]`

Dense and sparse retrieval are complementary: dense adds semantic generalization and sparse adds exact lexical

##### Child 1

**child_key:** `DOC-004::P004::Sparse Retrieval and BM25/Role::f68b5454a7a0::C001::b2cee934d85f`

**Child relevance:** `[   ]`

and sparse adds exact lexical precision.

### Document DOC-003

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-003::P000::Dense Retrieval::0b558e334b42`

**section_path:** Dense Retrieval

**Parent relevance:** `[   ]`

Document ID: DOC-003

##### Child 0

**child_key:** `DOC-003::P000::Dense Retrieval::0b558e334b42::C000::0b558e334b42`

**Child relevance:** `[   ]`

Document ID: DOC-003

#### Parent 1

**parent_key:** `DOC-003::P001::Dense Retrieval/Semantics::46ea4f15f99b`

**section_path:** Dense Retrieval > Semantics

**Parent relevance:** `[   ]`

Dense retrieval embeds queries and documents into vectors so semantically related text can match despite different wording. A query about making index construction more thorough can retrieve a passage about increasing ef_construct.

##### Child 0

**child_key:** `DOC-003::P001::Dense Retrieval/Semantics::46ea4f15f99b::C000::63abd5931c7c`

**Child relevance:** `[   ]`

Dense retrieval embeds queries and documents into vectors so semantically related text can match despite different

##### Child 1

**child_key:** `DOC-003::P001::Dense Retrieval/Semantics::46ea4f15f99b::C001::63d8602f3476`

**Child relevance:** `[   ]`

can match despite different wording. A query about making index construction more thorough can retrieve a passage about

##### Child 2

**child_key:** `DOC-003::P001::Dense Retrieval/Semantics::46ea4f15f99b::C002::d8899c1eb6b4`

**Child relevance:** `[   ]`

can retrieve a passage about increasing ef_construct.

#### Parent 2

**parent_key:** `DOC-003::P002::Dense Retrieval/Cosine::88a0b5f1f36a`

**section_path:** Dense Retrieval > Cosine

**Parent relevance:** `[   ]`

Cosine similarity measures geometric similarity, not the probability that a passage answers the question. Semantically related but non-answering passages can receive high scores.

##### Child 0

**child_key:** `DOC-003::P002::Dense Retrieval/Cosine::88a0b5f1f36a::C000::46281561c20e`

**Child relevance:** `[   ]`

Cosine similarity measures geometric similarity, not the probability that a passage answers the question. Semantically

##### Child 1

**child_key:** `DOC-003::P002::Dense Retrieval/Cosine::88a0b5f1f36a::C001::8b6e1f0c534a`

**Child relevance:** `[   ]`

the question. Semantically related but non-answering passages can receive high scores.

#### Parent 3

**parent_key:** `DOC-003::P003::Dense Retrieval/Weaknesses::c533c34f9468`

**section_path:** Dense Retrieval > Weaknesses

**Parent relevance:** `[   ]`

Opaque identifiers, error codes, version strings, and rare names such as uq_document_content_hash or ERR_CONNECTION_REFUSED can be difficult for a dense model.

##### Child 0

**child_key:** `DOC-003::P003::Dense Retrieval/Weaknesses::c533c34f9468::C000::8f9c410b4bc7`

**Child relevance:** `[   ]`

Opaque identifiers, error codes, version strings, and rare names such as uq_document_content_hash or

##### Child 1

**child_key:** `DOC-003::P003::Dense Retrieval/Weaknesses::c533c34f9468::C001::ddc89cd79486`

**Child relevance:** `[   ]`

as uq_document_content_hash or ERR_CONNECTION_REFUSED can be difficult for a dense model.

#### Parent 4

**parent_key:** `DOC-003::P004::Dense Retrieval/Breadth::48223e1d164a`

**section_path:** Dense Retrieval > Breadth

**Parent relevance:** `[   ]`

Candidate top_k controls recall opportunity. A later reranker cannot recover a relevant document that was removed before reranking.

##### Child 0

**child_key:** `DOC-003::P004::Dense Retrieval/Breadth::48223e1d164a::C000::94f15cc7fd50`

**Child relevance:** `[   ]`

Candidate top_k controls recall opportunity. A later reranker cannot recover a relevant document that was removed

##### Child 1

**child_key:** `DOC-003::P004::Dense Retrieval/Breadth::48223e1d164a::C001::0abd7d69c526`

**Child relevance:** `[   ]`

document that was removed before reranking.

---

## Q008

**Query:** Why shouldn't I add BM25 and cosine scores directly?

**Query class:** hybrid

**Answerability:** answerable

### Document DOC-005

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-005::P000::Hybrid Search and RRF::5664addb3f79`

**section_path:** Hybrid Search and RRF

**Parent relevance:** `[   ]`

Document ID: DOC-005

##### Child 0

**child_key:** `DOC-005::P000::Hybrid Search and RRF::5664addb3f79::C000::5664addb3f79`

**Child relevance:** `[   ]`

Document ID: DOC-005

#### Parent 1

**parent_key:** `DOC-005::P001::Hybrid Search and RRF/Hybrid::209328260861`

**section_path:** Hybrid Search and RRF > Hybrid

**Parent relevance:** `[   ]`

Hybrid retrieval runs dense and sparse searches for the same query and then fuses their candidate rankings.

##### Child 0

**child_key:** `DOC-005::P001::Hybrid Search and RRF/Hybrid::209328260861::C000::209328260861`

**Child relevance:** `[   ]`

Hybrid retrieval runs dense and sparse searches for the same query and then fuses their candidate rankings.

#### Parent 2

**parent_key:** `DOC-005::P002::Hybrid Search and RRF/RRF::fe8df2e00ff6`

**section_path:** Hybrid Search and RRF > RRF

**Parent relevance:** `[   ]`

Reciprocal Rank Fusion combines rank positions rather than raw cosine and BM25 magnitudes. A common contribution is 1 divided by k plus rank for each ranking containing the candidate.

##### Child 0

**child_key:** `DOC-005::P002::Hybrid Search and RRF/RRF::fe8df2e00ff6::C000::6438ac50137b`

**Child relevance:** `[   ]`

Reciprocal Rank Fusion combines rank positions rather than raw cosine and BM25 magnitudes. A common contribution is 1

##### Child 1

**child_key:** `DOC-005::P002::Hybrid Search and RRF/RRF::fe8df2e00ff6::C001::119dcfc67275`

**Child relevance:** `[   ]`

A common contribution is 1 divided by k plus rank for each ranking containing the candidate.

#### Parent 3

**parent_key:** `DOC-005::P003::Hybrid Search and RRF/Prefetch::749e43f445d1`

**section_path:** Hybrid Search and RRF > Prefetch

**Parent relevance:** `[   ]`

dense_prefetch_k and sparse_prefetch_k define how many candidates reach fusion. final_k defines how many fused results are returned. Fusion cannot recover items absent from both prefetch pools.

##### Child 0

**child_key:** `DOC-005::P003::Hybrid Search and RRF/Prefetch::749e43f445d1::C000::431ab3f75664`

**Child relevance:** `[   ]`

dense_prefetch_k and sparse_prefetch_k define how many candidates reach fusion. final_k defines how many fused results

##### Child 1

**child_key:** `DOC-005::P003::Hybrid Search and RRF/Prefetch::749e43f445d1::C001::f67f9829fa36`

**Child relevance:** `[   ]`

defines how many fused results are returned. Fusion cannot recover items absent from both prefetch pools.

#### Parent 4

**parent_key:** `DOC-005::P004::Hybrid Search and RRF/Caveat::6e10b63b70d4`

**section_path:** Hybrid Search and RRF > Caveat

**Parent relevance:** `[   ]`

RRF is robust because it avoids score calibration, but rank-only fusion discards information about how large the raw score gap was between adjacent candidates.

##### Child 0

**child_key:** `DOC-005::P004::Hybrid Search and RRF/Caveat::6e10b63b70d4::C000::bc447b0157ad`

**Child relevance:** `[   ]`

RRF is robust because it avoids score calibration, but rank-only fusion discards information about how large the raw

##### Child 1

**child_key:** `DOC-005::P004::Hybrid Search and RRF/Caveat::6e10b63b70d4::C001::2927773ffefe`

**Child relevance:** `[   ]`

about how large the raw score gap was between adjacent candidates.

### Document DOC-004

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-004::P000::Sparse Retrieval and BM25::2e408419645d`

**section_path:** Sparse Retrieval and BM25

**Parent relevance:** `[   ]`

Document ID: DOC-004

##### Child 0

**child_key:** `DOC-004::P000::Sparse Retrieval and BM25::2e408419645d::C000::2e408419645d`

**Child relevance:** `[   ]`

Document ID: DOC-004

#### Parent 1

**parent_key:** `DOC-004::P001::Sparse Retrieval and BM25/Lexical::85dbef0962d2`

**section_path:** Sparse Retrieval and BM25 > Lexical

**Parent relevance:** `[   ]`

BM25 uses explicit lexical evidence and rewards informative term matches while accounting for collection frequency and document length.

##### Child 0

**child_key:** `DOC-004::P001::Sparse Retrieval and BM25/Lexical::85dbef0962d2::C000::4be0fb0dd5f2`

**Child relevance:** `[   ]`

BM25 uses explicit lexical evidence and rewards informative term matches while accounting for collection frequency and

##### Child 1

**child_key:** `DOC-004::P001::Sparse Retrieval and BM25/Lexical::85dbef0962d2::C001::8451d40249b1`

**Child relevance:** `[   ]`

for collection frequency and document length.

#### Parent 2

**parent_key:** `DOC-004::P002::Sparse Retrieval and BM25/Identifiers::591b164e8bfc`

**section_path:** Sparse Retrieval and BM25 > Identifiers

**Parent relevance:** `[   ]`

Exact terms such as ef_construct, HTTP 422, tenant_id, vector_size, and uq_document_content_hash are strong sparse-search signals.

##### Child 0

**child_key:** `DOC-004::P002::Sparse Retrieval and BM25/Identifiers::591b164e8bfc::C000::7b2b4c61478c`

**Child relevance:** `[   ]`

Exact terms such as ef_construct, HTTP 422, tenant_id, vector_size, and uq_document_content_hash are strong

##### Child 1

**child_key:** `DOC-004::P002::Sparse Retrieval and BM25/Identifiers::591b164e8bfc::C001::359bc6fc3d42`

**Child relevance:** `[   ]`

are strong sparse-search signals.

#### Parent 3

**parent_key:** `DOC-004::P003::Sparse Retrieval and BM25/Limit::2667a2c792be`

**section_path:** Sparse Retrieval and BM25 > Limit

**Parent relevance:** `[   ]`

Sparse retrieval does not generalize paraphrases like a dense model. Build phase and index construction may refer to the same concept without sharing the same terms.

##### Child 0

**child_key:** `DOC-004::P003::Sparse Retrieval and BM25/Limit::2667a2c792be::C000::e4a57921ae4e`

**Child relevance:** `[   ]`

Sparse retrieval does not generalize paraphrases like a dense model. Build phase and index construction may refer to

##### Child 1

**child_key:** `DOC-004::P003::Sparse Retrieval and BM25/Limit::2667a2c792be::C001::d1d1320a8897`

**Child relevance:** `[   ]`

construction may refer to the same concept without sharing the same terms.

#### Parent 4

**parent_key:** `DOC-004::P004::Sparse Retrieval and BM25/Role::f68b5454a7a0`

**section_path:** Sparse Retrieval and BM25 > Role

**Parent relevance:** `[   ]`

Dense and sparse retrieval are complementary: dense adds semantic generalization and sparse adds exact lexical precision.

##### Child 0

**child_key:** `DOC-004::P004::Sparse Retrieval and BM25/Role::f68b5454a7a0::C000::d8c291559660`

**Child relevance:** `[   ]`

Dense and sparse retrieval are complementary: dense adds semantic generalization and sparse adds exact lexical

##### Child 1

**child_key:** `DOC-004::P004::Sparse Retrieval and BM25/Role::f68b5454a7a0::C001::b2cee934d85f`

**Child relevance:** `[   ]`

and sparse adds exact lexical precision.

---

## Q009

**Query:** What is the difference between prefetch_k and final_k?

**Query class:** configuration

**Answerability:** answerable

### Document DOC-005

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-005::P000::Hybrid Search and RRF::5664addb3f79`

**section_path:** Hybrid Search and RRF

**Parent relevance:** `[   ]`

Document ID: DOC-005

##### Child 0

**child_key:** `DOC-005::P000::Hybrid Search and RRF::5664addb3f79::C000::5664addb3f79`

**Child relevance:** `[   ]`

Document ID: DOC-005

#### Parent 1

**parent_key:** `DOC-005::P001::Hybrid Search and RRF/Hybrid::209328260861`

**section_path:** Hybrid Search and RRF > Hybrid

**Parent relevance:** `[   ]`

Hybrid retrieval runs dense and sparse searches for the same query and then fuses their candidate rankings.

##### Child 0

**child_key:** `DOC-005::P001::Hybrid Search and RRF/Hybrid::209328260861::C000::209328260861`

**Child relevance:** `[   ]`

Hybrid retrieval runs dense and sparse searches for the same query and then fuses their candidate rankings.

#### Parent 2

**parent_key:** `DOC-005::P002::Hybrid Search and RRF/RRF::fe8df2e00ff6`

**section_path:** Hybrid Search and RRF > RRF

**Parent relevance:** `[   ]`

Reciprocal Rank Fusion combines rank positions rather than raw cosine and BM25 magnitudes. A common contribution is 1 divided by k plus rank for each ranking containing the candidate.

##### Child 0

**child_key:** `DOC-005::P002::Hybrid Search and RRF/RRF::fe8df2e00ff6::C000::6438ac50137b`

**Child relevance:** `[   ]`

Reciprocal Rank Fusion combines rank positions rather than raw cosine and BM25 magnitudes. A common contribution is 1

##### Child 1

**child_key:** `DOC-005::P002::Hybrid Search and RRF/RRF::fe8df2e00ff6::C001::119dcfc67275`

**Child relevance:** `[   ]`

A common contribution is 1 divided by k plus rank for each ranking containing the candidate.

#### Parent 3

**parent_key:** `DOC-005::P003::Hybrid Search and RRF/Prefetch::749e43f445d1`

**section_path:** Hybrid Search and RRF > Prefetch

**Parent relevance:** `[   ]`

dense_prefetch_k and sparse_prefetch_k define how many candidates reach fusion. final_k defines how many fused results are returned. Fusion cannot recover items absent from both prefetch pools.

##### Child 0

**child_key:** `DOC-005::P003::Hybrid Search and RRF/Prefetch::749e43f445d1::C000::431ab3f75664`

**Child relevance:** `[   ]`

dense_prefetch_k and sparse_prefetch_k define how many candidates reach fusion. final_k defines how many fused results

##### Child 1

**child_key:** `DOC-005::P003::Hybrid Search and RRF/Prefetch::749e43f445d1::C001::f67f9829fa36`

**Child relevance:** `[   ]`

defines how many fused results are returned. Fusion cannot recover items absent from both prefetch pools.

#### Parent 4

**parent_key:** `DOC-005::P004::Hybrid Search and RRF/Caveat::6e10b63b70d4`

**section_path:** Hybrid Search and RRF > Caveat

**Parent relevance:** `[   ]`

RRF is robust because it avoids score calibration, but rank-only fusion discards information about how large the raw score gap was between adjacent candidates.

##### Child 0

**child_key:** `DOC-005::P004::Hybrid Search and RRF/Caveat::6e10b63b70d4::C000::bc447b0157ad`

**Child relevance:** `[   ]`

RRF is robust because it avoids score calibration, but rank-only fusion discards information about how large the raw

##### Child 1

**child_key:** `DOC-005::P004::Hybrid Search and RRF/Caveat::6e10b63b70d4::C001::2927773ffefe`

**Child relevance:** `[   ]`

about how large the raw score gap was between adjacent candidates.

---

## Q010

**Query:** Why should children be created from persisted parents?

**Query class:** architecture

**Answerability:** answerable

### Document DOC-006

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-006::P000::Parent Child Retrieval::b35088d41309`

**section_path:** Parent Child Retrieval

**Parent relevance:** `[   ]`

Document ID: DOC-006

##### Child 0

**child_key:** `DOC-006::P000::Parent Child Retrieval::b35088d41309::C000::b35088d41309`

**Child relevance:** `[   ]`

Document ID: DOC-006

#### Parent 1

**parent_key:** `DOC-006::P001::Parent Child Retrieval/Purpose::58f2e1646f06`

**section_path:** Parent Child Retrieval > Purpose

**Parent relevance:** `[   ]`

Small child chunks improve retrieval precision while larger parent chunks restore context for the language model.

##### Child 0

**child_key:** `DOC-006::P001::Parent Child Retrieval/Purpose::58f2e1646f06::C000::58f2e1646f06`

**Child relevance:** `[   ]`

Small child chunks improve retrieval precision while larger parent chunks restore context for the language model.

#### Parent 2

**parent_key:** `DOC-006::P002::Parent Child Retrieval/Identity::056fc40a43ef`

**section_path:** Parent Child Retrieval > Identity

**Parent relevance:** `[   ]`

Each child must reference an authoritative persisted parent_id. Generating children from temporary parents can create dangling references if persisted IDs differ.

##### Child 0

**child_key:** `DOC-006::P002::Parent Child Retrieval/Identity::056fc40a43ef::C000::835b5886e0cf`

**Child relevance:** `[   ]`

Each child must reference an authoritative persisted parent_id. Generating children from temporary parents can create

##### Child 1

**child_key:** `DOC-006::P002::Parent Child Retrieval/Identity::056fc40a43ef::C001::ea85c1b95a87`

**Child relevance:** `[   ]`

temporary parents can create dangling references if persisted IDs differ.

#### Parent 3

**parent_key:** `DOC-006::P003::Parent Child Retrieval/Dedup::b7ed0d561239`

**section_path:** Parent Child Retrieval > Dedup

**Parent relevance:** `[   ]`

Multiple child hits can belong to one parent, so parent expansion groups by parent_id and fetches the parent once while retaining matched-child evidence for debugging.

##### Child 0

**child_key:** `DOC-006::P003::Parent Child Retrieval/Dedup::b7ed0d561239::C000::d1bd65315d93`

**Child relevance:** `[   ]`

Multiple child hits can belong to one parent, so parent expansion groups by parent_id and fetches the parent once while

##### Child 1

**child_key:** `DOC-006::P003::Parent Child Retrieval/Dedup::b7ed0d561239::C001::0aaa0f6b6d03`

**Child relevance:** `[   ]`

fetches the parent once while retaining matched-child evidence for debugging.

#### Parent 4

**parent_key:** `DOC-006::P004::Parent Child Retrieval/Trade-off::c49ad4b99a52`

**section_path:** Parent Child Retrieval > Trade-off

**Parent relevance:** `[   ]`

Parent child retrieval increases synchronization complexity but is valuable when the best retrieval unit is smaller than the best generation context unit.

##### Child 0

**child_key:** `DOC-006::P004::Parent Child Retrieval/Trade-off::c49ad4b99a52::C000::95b65bb60d44`

**Child relevance:** `[   ]`

Parent child retrieval increases synchronization complexity but is valuable when the best retrieval unit is smaller

##### Child 1

**child_key:** `DOC-006::P004::Parent Child Retrieval/Trade-off::c49ad4b99a52::C001::05cc04a5ec7d`

**Child relevance:** `[   ]`

best retrieval unit is smaller than the best generation context unit.

### Document DOC-013

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-013::P000::MongoDB Parent Repository::bd3b4b66f1b8`

**section_path:** MongoDB Parent Repository

**Parent relevance:** `[   ]`

Document ID: DOC-013

##### Child 0

**child_key:** `DOC-013::P000::MongoDB Parent Repository::bd3b4b66f1b8::C000::bd3b4b66f1b8`

**Child relevance:** `[   ]`

Document ID: DOC-013

#### Parent 1

**parent_key:** `DOC-013::P001::MongoDB Parent Repository/Store::fccc07403250`

**section_path:** MongoDB Parent Repository > Store

**Parent relevance:** `[   ]`

MongoDB can hold authoritative ParentChunk records while Qdrant stores searchable child representations.

##### Child 0

**child_key:** `DOC-013::P001::MongoDB Parent Repository/Store::fccc07403250::C000::fccc07403250`

**Child relevance:** `[   ]`

MongoDB can hold authoritative ParentChunk records while Qdrant stores searchable child representations.

#### Parent 2

**parent_key:** `DOC-013::P002::MongoDB Parent Repository/Indexes::22da8c0b400f`

**section_path:** MongoDB Parent Repository > Indexes

**Parent relevance:** `[   ]`

A compound unique index on document_id and content_hash can prevent duplicate logical parent content. Conflicting existing index options can produce IndexOptionsConflict.

##### Child 0

**child_key:** `DOC-013::P002::MongoDB Parent Repository/Indexes::22da8c0b400f::C000::8066d47e6e78`

**Child relevance:** `[   ]`

A compound unique index on document_id and content_hash can prevent duplicate logical parent content. Conflicting

##### Child 1

**child_key:** `DOC-013::P002::MongoDB Parent Repository/Indexes::22da8c0b400f::C001::469f1e25137b`

**Child relevance:** `[   ]`

parent content. Conflicting existing index options can produce IndexOptionsConflict.

#### Parent 3

**parent_key:** `DOC-013::P003::MongoDB Parent Repository/Sync::0f317eaa9724`

**section_path:** MongoDB Parent Repository > Sync

**Parent relevance:** `[   ]`

Parent synchronization inserts new parents, preserves unchanged persisted identifiers, and deletes stale parents based on content hashes.

##### Child 0

**child_key:** `DOC-013::P003::MongoDB Parent Repository/Sync::0f317eaa9724::C000::4d3db31af3e2`

**Child relevance:** `[   ]`

Parent synchronization inserts new parents, preserves unchanged persisted identifiers, and deletes stale parents based

##### Child 1

**child_key:** `DOC-013::P003::MongoDB Parent Repository/Sync::0f317eaa9724::C001::07ffde0db481`

**Child relevance:** `[   ]`

deletes stale parents based on content hashes.

#### Parent 4

**parent_key:** `DOC-013::P004::MongoDB Parent Repository/Lookup::78ba0de4419e`

**section_path:** MongoDB Parent Repository > Lookup

**Parent relevance:** `[   ]`

Children should be generated from persisted parents and parent expansion should fail loudly when a referenced parent is missing.

##### Child 0

**child_key:** `DOC-013::P004::MongoDB Parent Repository/Lookup::78ba0de4419e::C000::4fb647181fc1`

**Child relevance:** `[   ]`

Children should be generated from persisted parents and parent expansion should fail loudly when a referenced parent is

##### Child 1

**child_key:** `DOC-013::P004::MongoDB Parent Repository/Lookup::78ba0de4419e::C001::bfc95860d7cf`

**Child relevance:** `[   ]`

when a referenced parent is missing.

---

## Q011

**Query:** What is a dangling parent reference?

**Query class:** failure mode

**Answerability:** answerable

### Document DOC-006

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-006::P000::Parent Child Retrieval::b35088d41309`

**section_path:** Parent Child Retrieval

**Parent relevance:** `[   ]`

Document ID: DOC-006

##### Child 0

**child_key:** `DOC-006::P000::Parent Child Retrieval::b35088d41309::C000::b35088d41309`

**Child relevance:** `[   ]`

Document ID: DOC-006

#### Parent 1

**parent_key:** `DOC-006::P001::Parent Child Retrieval/Purpose::58f2e1646f06`

**section_path:** Parent Child Retrieval > Purpose

**Parent relevance:** `[   ]`

Small child chunks improve retrieval precision while larger parent chunks restore context for the language model.

##### Child 0

**child_key:** `DOC-006::P001::Parent Child Retrieval/Purpose::58f2e1646f06::C000::58f2e1646f06`

**Child relevance:** `[   ]`

Small child chunks improve retrieval precision while larger parent chunks restore context for the language model.

#### Parent 2

**parent_key:** `DOC-006::P002::Parent Child Retrieval/Identity::056fc40a43ef`

**section_path:** Parent Child Retrieval > Identity

**Parent relevance:** `[   ]`

Each child must reference an authoritative persisted parent_id. Generating children from temporary parents can create dangling references if persisted IDs differ.

##### Child 0

**child_key:** `DOC-006::P002::Parent Child Retrieval/Identity::056fc40a43ef::C000::835b5886e0cf`

**Child relevance:** `[   ]`

Each child must reference an authoritative persisted parent_id. Generating children from temporary parents can create

##### Child 1

**child_key:** `DOC-006::P002::Parent Child Retrieval/Identity::056fc40a43ef::C001::ea85c1b95a87`

**Child relevance:** `[   ]`

temporary parents can create dangling references if persisted IDs differ.

#### Parent 3

**parent_key:** `DOC-006::P003::Parent Child Retrieval/Dedup::b7ed0d561239`

**section_path:** Parent Child Retrieval > Dedup

**Parent relevance:** `[   ]`

Multiple child hits can belong to one parent, so parent expansion groups by parent_id and fetches the parent once while retaining matched-child evidence for debugging.

##### Child 0

**child_key:** `DOC-006::P003::Parent Child Retrieval/Dedup::b7ed0d561239::C000::d1bd65315d93`

**Child relevance:** `[   ]`

Multiple child hits can belong to one parent, so parent expansion groups by parent_id and fetches the parent once while

##### Child 1

**child_key:** `DOC-006::P003::Parent Child Retrieval/Dedup::b7ed0d561239::C001::0aaa0f6b6d03`

**Child relevance:** `[   ]`

fetches the parent once while retaining matched-child evidence for debugging.

#### Parent 4

**parent_key:** `DOC-006::P004::Parent Child Retrieval/Trade-off::c49ad4b99a52`

**section_path:** Parent Child Retrieval > Trade-off

**Parent relevance:** `[   ]`

Parent child retrieval increases synchronization complexity but is valuable when the best retrieval unit is smaller than the best generation context unit.

##### Child 0

**child_key:** `DOC-006::P004::Parent Child Retrieval/Trade-off::c49ad4b99a52::C000::95b65bb60d44`

**Child relevance:** `[   ]`

Parent child retrieval increases synchronization complexity but is valuable when the best retrieval unit is smaller

##### Child 1

**child_key:** `DOC-006::P004::Parent Child Retrieval/Trade-off::c49ad4b99a52::C001::05cc04a5ec7d`

**Child relevance:** `[   ]`

best retrieval unit is smaller than the best generation context unit.

### Document DOC-012

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-012::P000::Qdrant Synchronization::a18f6359ba4c`

**section_path:** Qdrant Synchronization

**Parent relevance:** `[   ]`

Document ID: DOC-012

##### Child 0

**child_key:** `DOC-012::P000::Qdrant Synchronization::a18f6359ba4c::C000::a18f6359ba4c`

**Child relevance:** `[   ]`

Document ID: DOC-012

#### Parent 1

**parent_key:** `DOC-012::P001::Qdrant Synchronization/Idempotency::21e92ae60327`

**section_path:** Qdrant Synchronization > Idempotency

**Parent relevance:** `[   ]`

Repeated ingestion of unchanged source content should not create duplicate logical child points.

##### Child 0

**child_key:** `DOC-012::P001::Qdrant Synchronization/Idempotency::21e92ae60327::C000::21e92ae60327`

**Child relevance:** `[   ]`

Repeated ingestion of unchanged source content should not create duplicate logical child points.

#### Parent 2

**parent_key:** `DOC-012::P002::Qdrant Synchronization/Coarse sync::8eeba34c4f89`

**section_path:** Qdrant Synchronization > Coarse sync

**Parent relevance:** `[   ]`

Delete-all-then-reinsert synchronization is current-state correct but recomputes and rewrites unchanged vectors.

##### Child 0

**child_key:** `DOC-012::P002::Qdrant Synchronization/Coarse sync::8eeba34c4f89::C000::8eeba34c4f89`

**Child relevance:** `[   ]`

Delete-all-then-reinsert synchronization is current-state correct but recomputes and rewrites unchanged vectors.

#### Parent 3

**parent_key:** `DOC-012::P003::Qdrant Synchronization/Differential::e494d1bad168`

**section_path:** Qdrant Synchronization > Differential

**Parent relevance:** `[   ]`

Differential synchronization preserves unchanged children, inserts new or changed children, and deletes stale children. An unchanged run should approach inserted=0, unchanged=N, stale_deleted=0.

##### Child 0

**child_key:** `DOC-012::P003::Qdrant Synchronization/Differential::e494d1bad168::C000::a6be7b76f898`

**Child relevance:** `[   ]`

Differential synchronization preserves unchanged children, inserts new or changed children, and deletes stale children.

##### Child 1

**child_key:** `DOC-012::P003::Qdrant Synchronization/Differential::e494d1bad168::C001::e2aaff858b62`

**Child relevance:** `[   ]`

and deletes stale children. An unchanged run should approach inserted=0, unchanged=N, stale_deleted=0.

#### Parent 4

**parent_key:** `DOC-012::P004::Qdrant Synchronization/Dangling::a94ff5f0450e`

**section_path:** Qdrant Synchronization > Dangling

**Parent relevance:** `[   ]`

Old Qdrant children can reference parents that MongoDB no longer contains. Parent expansion should detect this integrity failure.

##### Child 0

**child_key:** `DOC-012::P004::Qdrant Synchronization/Dangling::a94ff5f0450e::C000::8a10e11f1b5b`

**Child relevance:** `[   ]`

Old Qdrant children can reference parents that MongoDB no longer contains. Parent expansion should detect this

##### Child 1

**child_key:** `DOC-012::P004::Qdrant Synchronization/Dangling::a94ff5f0450e::C001::a75bb71c1249`

**Child relevance:** `[   ]`

expansion should detect this integrity failure.

### Document DOC-013

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-013::P000::MongoDB Parent Repository::bd3b4b66f1b8`

**section_path:** MongoDB Parent Repository

**Parent relevance:** `[   ]`

Document ID: DOC-013

##### Child 0

**child_key:** `DOC-013::P000::MongoDB Parent Repository::bd3b4b66f1b8::C000::bd3b4b66f1b8`

**Child relevance:** `[   ]`

Document ID: DOC-013

#### Parent 1

**parent_key:** `DOC-013::P001::MongoDB Parent Repository/Store::fccc07403250`

**section_path:** MongoDB Parent Repository > Store

**Parent relevance:** `[   ]`

MongoDB can hold authoritative ParentChunk records while Qdrant stores searchable child representations.

##### Child 0

**child_key:** `DOC-013::P001::MongoDB Parent Repository/Store::fccc07403250::C000::fccc07403250`

**Child relevance:** `[   ]`

MongoDB can hold authoritative ParentChunk records while Qdrant stores searchable child representations.

#### Parent 2

**parent_key:** `DOC-013::P002::MongoDB Parent Repository/Indexes::22da8c0b400f`

**section_path:** MongoDB Parent Repository > Indexes

**Parent relevance:** `[   ]`

A compound unique index on document_id and content_hash can prevent duplicate logical parent content. Conflicting existing index options can produce IndexOptionsConflict.

##### Child 0

**child_key:** `DOC-013::P002::MongoDB Parent Repository/Indexes::22da8c0b400f::C000::8066d47e6e78`

**Child relevance:** `[   ]`

A compound unique index on document_id and content_hash can prevent duplicate logical parent content. Conflicting

##### Child 1

**child_key:** `DOC-013::P002::MongoDB Parent Repository/Indexes::22da8c0b400f::C001::469f1e25137b`

**Child relevance:** `[   ]`

parent content. Conflicting existing index options can produce IndexOptionsConflict.

#### Parent 3

**parent_key:** `DOC-013::P003::MongoDB Parent Repository/Sync::0f317eaa9724`

**section_path:** MongoDB Parent Repository > Sync

**Parent relevance:** `[   ]`

Parent synchronization inserts new parents, preserves unchanged persisted identifiers, and deletes stale parents based on content hashes.

##### Child 0

**child_key:** `DOC-013::P003::MongoDB Parent Repository/Sync::0f317eaa9724::C000::4d3db31af3e2`

**Child relevance:** `[   ]`

Parent synchronization inserts new parents, preserves unchanged persisted identifiers, and deletes stale parents based

##### Child 1

**child_key:** `DOC-013::P003::MongoDB Parent Repository/Sync::0f317eaa9724::C001::07ffde0db481`

**Child relevance:** `[   ]`

deletes stale parents based on content hashes.

#### Parent 4

**parent_key:** `DOC-013::P004::MongoDB Parent Repository/Lookup::78ba0de4419e`

**section_path:** MongoDB Parent Repository > Lookup

**Parent relevance:** `[   ]`

Children should be generated from persisted parents and parent expansion should fail loudly when a referenced parent is missing.

##### Child 0

**child_key:** `DOC-013::P004::MongoDB Parent Repository/Lookup::78ba0de4419e::C000::4fb647181fc1`

**Child relevance:** `[   ]`

Children should be generated from persisted parents and parent expansion should fail loudly when a referenced parent is

##### Child 1

**child_key:** `DOC-013::P004::MongoDB Parent Repository/Lookup::78ba0de4419e::C001::bfc95860d7cf`

**Child relevance:** `[   ]`

when a referenced parent is missing.

---

## Q012

**Query:** Why rerank parents with a CrossEncoder?

**Query class:** reranking

**Answerability:** answerable

### Document DOC-007

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-007::P000::CrossEncoder Reranking::0bf4b5893750`

**section_path:** CrossEncoder Reranking

**Parent relevance:** `[   ]`

Document ID: DOC-007

##### Child 0

**child_key:** `DOC-007::P000::CrossEncoder Reranking::0bf4b5893750::C000::0bf4b5893750`

**Child relevance:** `[   ]`

Document ID: DOC-007

#### Parent 1

**parent_key:** `DOC-007::P001::CrossEncoder Reranking/Scoring::c07aae2dd2b3`

**section_path:** CrossEncoder Reranking > Scoring

**Parent relevance:** `[   ]`

A CrossEncoder jointly processes query and candidate text, allowing deeper query-document interaction than independent embeddings.

##### Child 0

**child_key:** `DOC-007::P001::CrossEncoder Reranking/Scoring::c07aae2dd2b3::C000::6e465d447abe`

**Child relevance:** `[   ]`

A CrossEncoder jointly processes query and candidate text, allowing deeper query-document interaction than independent

##### Child 1

**child_key:** `DOC-007::P001::CrossEncoder Reranking/Scoring::c07aae2dd2b3::C001::0f1c48345abd`

**Child relevance:** `[   ]`

interaction than independent embeddings.

#### Parent 2

**parent_key:** `DOC-007::P002::CrossEncoder Reranking/Placement::5db9debefc4d`

**section_path:** CrossEncoder Reranking > Placement

**Parent relevance:** `[   ]`

CrossEncoder reranking follows broad first-stage retrieval because pairwise inference is more expensive. Missing candidates cannot be recovered.

##### Child 0

**child_key:** `DOC-007::P002::CrossEncoder Reranking/Placement::5db9debefc4d::C000::a49c242c244a`

**Child relevance:** `[   ]`

CrossEncoder reranking follows broad first-stage retrieval because pairwise inference is more expensive. Missing

##### Child 1

**child_key:** `DOC-007::P002::CrossEncoder Reranking/Placement::5db9debefc4d::C001::6404fe72d734`

**Child relevance:** `[   ]`

is more expensive. Missing candidates cannot be recovered.

#### Parent 3

**parent_key:** `DOC-007::P003::CrossEncoder Reranking/Calibration::a3381d0856c9`

**section_path:** CrossEncoder Reranking > Calibration

**Parent relevance:** `[   ]`

CrossEncoder outputs should not automatically be treated as universally calibrated probabilities. Query phrasing can change scores substantially.

##### Child 0

**child_key:** `DOC-007::P003::CrossEncoder Reranking/Calibration::a3381d0856c9::C000::09f70b54e350`

**Child relevance:** `[   ]`

CrossEncoder outputs should not automatically be treated as universally calibrated probabilities. Query phrasing can

##### Child 1

**child_key:** `DOC-007::P003::CrossEncoder Reranking/Calibration::a3381d0856c9::C001::e9f6b58ae07c`

**Child relevance:** `[   ]`

Query phrasing can change scores substantially.

#### Parent 4

**parent_key:** `DOC-007::P004::CrossEncoder Reranking/Parents::3ca6d613f1f0`

**section_path:** CrossEncoder Reranking > Parents

**Parent relevance:** `[   ]`

In parent child RAG, a useful pattern retrieves children, expands parents, then reranks full ParentChunk content.

##### Child 0

**child_key:** `DOC-007::P004::CrossEncoder Reranking/Parents::3ca6d613f1f0::C000::3ca6d613f1f0`

**Child relevance:** `[   ]`

In parent child RAG, a useful pattern retrieves children, expands parents, then reranks full ParentChunk content.

### Document DOC-006

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-006::P000::Parent Child Retrieval::b35088d41309`

**section_path:** Parent Child Retrieval

**Parent relevance:** `[   ]`

Document ID: DOC-006

##### Child 0

**child_key:** `DOC-006::P000::Parent Child Retrieval::b35088d41309::C000::b35088d41309`

**Child relevance:** `[   ]`

Document ID: DOC-006

#### Parent 1

**parent_key:** `DOC-006::P001::Parent Child Retrieval/Purpose::58f2e1646f06`

**section_path:** Parent Child Retrieval > Purpose

**Parent relevance:** `[   ]`

Small child chunks improve retrieval precision while larger parent chunks restore context for the language model.

##### Child 0

**child_key:** `DOC-006::P001::Parent Child Retrieval/Purpose::58f2e1646f06::C000::58f2e1646f06`

**Child relevance:** `[   ]`

Small child chunks improve retrieval precision while larger parent chunks restore context for the language model.

#### Parent 2

**parent_key:** `DOC-006::P002::Parent Child Retrieval/Identity::056fc40a43ef`

**section_path:** Parent Child Retrieval > Identity

**Parent relevance:** `[   ]`

Each child must reference an authoritative persisted parent_id. Generating children from temporary parents can create dangling references if persisted IDs differ.

##### Child 0

**child_key:** `DOC-006::P002::Parent Child Retrieval/Identity::056fc40a43ef::C000::835b5886e0cf`

**Child relevance:** `[   ]`

Each child must reference an authoritative persisted parent_id. Generating children from temporary parents can create

##### Child 1

**child_key:** `DOC-006::P002::Parent Child Retrieval/Identity::056fc40a43ef::C001::ea85c1b95a87`

**Child relevance:** `[   ]`

temporary parents can create dangling references if persisted IDs differ.

#### Parent 3

**parent_key:** `DOC-006::P003::Parent Child Retrieval/Dedup::b7ed0d561239`

**section_path:** Parent Child Retrieval > Dedup

**Parent relevance:** `[   ]`

Multiple child hits can belong to one parent, so parent expansion groups by parent_id and fetches the parent once while retaining matched-child evidence for debugging.

##### Child 0

**child_key:** `DOC-006::P003::Parent Child Retrieval/Dedup::b7ed0d561239::C000::d1bd65315d93`

**Child relevance:** `[   ]`

Multiple child hits can belong to one parent, so parent expansion groups by parent_id and fetches the parent once while

##### Child 1

**child_key:** `DOC-006::P003::Parent Child Retrieval/Dedup::b7ed0d561239::C001::0aaa0f6b6d03`

**Child relevance:** `[   ]`

fetches the parent once while retaining matched-child evidence for debugging.

#### Parent 4

**parent_key:** `DOC-006::P004::Parent Child Retrieval/Trade-off::c49ad4b99a52`

**section_path:** Parent Child Retrieval > Trade-off

**Parent relevance:** `[   ]`

Parent child retrieval increases synchronization complexity but is valuable when the best retrieval unit is smaller than the best generation context unit.

##### Child 0

**child_key:** `DOC-006::P004::Parent Child Retrieval/Trade-off::c49ad4b99a52::C000::95b65bb60d44`

**Child relevance:** `[   ]`

Parent child retrieval increases synchronization complexity but is valuable when the best retrieval unit is smaller

##### Child 1

**child_key:** `DOC-006::P004::Parent Child Retrieval/Trade-off::c49ad4b99a52::C001::05cc04a5ec7d`

**Child relevance:** `[   ]`

best retrieval unit is smaller than the best generation context unit.

---

## Q013

**Query:** Can I treat a CrossEncoder sigmoid score as a calibrated probability?

**Query class:** score semantics

**Answerability:** answerable

### Document DOC-007

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-007::P000::CrossEncoder Reranking::0bf4b5893750`

**section_path:** CrossEncoder Reranking

**Parent relevance:** `[   ]`

Document ID: DOC-007

##### Child 0

**child_key:** `DOC-007::P000::CrossEncoder Reranking::0bf4b5893750::C000::0bf4b5893750`

**Child relevance:** `[   ]`

Document ID: DOC-007

#### Parent 1

**parent_key:** `DOC-007::P001::CrossEncoder Reranking/Scoring::c07aae2dd2b3`

**section_path:** CrossEncoder Reranking > Scoring

**Parent relevance:** `[   ]`

A CrossEncoder jointly processes query and candidate text, allowing deeper query-document interaction than independent embeddings.

##### Child 0

**child_key:** `DOC-007::P001::CrossEncoder Reranking/Scoring::c07aae2dd2b3::C000::6e465d447abe`

**Child relevance:** `[   ]`

A CrossEncoder jointly processes query and candidate text, allowing deeper query-document interaction than independent

##### Child 1

**child_key:** `DOC-007::P001::CrossEncoder Reranking/Scoring::c07aae2dd2b3::C001::0f1c48345abd`

**Child relevance:** `[   ]`

interaction than independent embeddings.

#### Parent 2

**parent_key:** `DOC-007::P002::CrossEncoder Reranking/Placement::5db9debefc4d`

**section_path:** CrossEncoder Reranking > Placement

**Parent relevance:** `[   ]`

CrossEncoder reranking follows broad first-stage retrieval because pairwise inference is more expensive. Missing candidates cannot be recovered.

##### Child 0

**child_key:** `DOC-007::P002::CrossEncoder Reranking/Placement::5db9debefc4d::C000::a49c242c244a`

**Child relevance:** `[   ]`

CrossEncoder reranking follows broad first-stage retrieval because pairwise inference is more expensive. Missing

##### Child 1

**child_key:** `DOC-007::P002::CrossEncoder Reranking/Placement::5db9debefc4d::C001::6404fe72d734`

**Child relevance:** `[   ]`

is more expensive. Missing candidates cannot be recovered.

#### Parent 3

**parent_key:** `DOC-007::P003::CrossEncoder Reranking/Calibration::a3381d0856c9`

**section_path:** CrossEncoder Reranking > Calibration

**Parent relevance:** `[   ]`

CrossEncoder outputs should not automatically be treated as universally calibrated probabilities. Query phrasing can change scores substantially.

##### Child 0

**child_key:** `DOC-007::P003::CrossEncoder Reranking/Calibration::a3381d0856c9::C000::09f70b54e350`

**Child relevance:** `[   ]`

CrossEncoder outputs should not automatically be treated as universally calibrated probabilities. Query phrasing can

##### Child 1

**child_key:** `DOC-007::P003::CrossEncoder Reranking/Calibration::a3381d0856c9::C001::e9f6b58ae07c`

**Child relevance:** `[   ]`

Query phrasing can change scores substantially.

#### Parent 4

**parent_key:** `DOC-007::P004::CrossEncoder Reranking/Parents::3ca6d613f1f0`

**section_path:** CrossEncoder Reranking > Parents

**Parent relevance:** `[   ]`

In parent child RAG, a useful pattern retrieves children, expands parents, then reranks full ParentChunk content.

##### Child 0

**child_key:** `DOC-007::P004::CrossEncoder Reranking/Parents::3ca6d613f1f0::C000::3ca6d613f1f0`

**Child relevance:** `[   ]`

In parent child RAG, a useful pattern retrieves children, expands parents, then reranks full ParentChunk content.

---

## Q014

**Query:** Why not mix CrossEncoder scores directly with cosine redundancy in MMR?

**Query class:** MMR

**Answerability:** answerable

### Document DOC-008

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-008::P000::Maximal Marginal Relevance::fd1e2333d88d`

**section_path:** Maximal Marginal Relevance

**Parent relevance:** `[   ]`

Document ID: DOC-008

##### Child 0

**child_key:** `DOC-008::P000::Maximal Marginal Relevance::fd1e2333d88d::C000::fd1e2333d88d`

**Child relevance:** `[   ]`

Document ID: DOC-008

#### Parent 1

**parent_key:** `DOC-008::P001::Maximal Marginal Relevance/Formula::7ca32192b588`

**section_path:** Maximal Marginal Relevance > Formula

**Parent relevance:** `[   ]`

MMR balances query relevance against redundancy with already selected items. A typical objective is lambda times relevance minus one minus lambda times maximum redundancy.

##### Child 0

**child_key:** `DOC-008::P001::Maximal Marginal Relevance/Formula::7ca32192b588::C000::2cbb321f3ebb`

**Child relevance:** `[   ]`

MMR balances query relevance against redundancy with already selected items. A typical objective is lambda times

##### Child 1

**child_key:** `DOC-008::P001::Maximal Marginal Relevance/Formula::7ca32192b588::C001::d0e50a39be35`

**Child relevance:** `[   ]`

objective is lambda times relevance minus one minus lambda times maximum redundancy.

#### Parent 2

**parent_key:** `DOC-008::P002::Maximal Marginal Relevance/Lambda::b180418cbc42`

**section_path:** Maximal Marginal Relevance > Lambda

**Parent relevance:** `[   ]`

Lambda near one favors relevance. Lower lambda increases diversity, but an excessively low value may promote unusual yet weakly relevant items.

##### Child 0

**child_key:** `DOC-008::P002::Maximal Marginal Relevance/Lambda::b180418cbc42::C000::7cd845361496`

**Child relevance:** `[   ]`

Lambda near one favors relevance. Lower lambda increases diversity, but an excessively low value may promote unusual

##### Child 1

**child_key:** `DOC-008::P002::Maximal Marginal Relevance/Lambda::b180418cbc42::C001::853c1cd928a1`

**Child relevance:** `[   ]`

low value may promote unusual yet weakly relevant items.

#### Parent 3

**parent_key:** `DOC-008::P003::Maximal Marginal Relevance/Space::fab69a871cbf`

**section_path:** Maximal Marginal Relevance > Space

**Parent relevance:** `[   ]`

Dense parent MMR should compute relevance and redundancy in the same embedding space. Mixing CrossEncoder values directly with cosine redundancy is not calibrated.

##### Child 0

**child_key:** `DOC-008::P003::Maximal Marginal Relevance/Space::fab69a871cbf::C000::2801da19fbbe`

**Child relevance:** `[   ]`

Dense parent MMR should compute relevance and redundancy in the same embedding space. Mixing CrossEncoder values

##### Child 1

**child_key:** `DOC-008::P003::Maximal Marginal Relevance/Space::fab69a871cbf::C001::1dba5e9f5764`

**Child relevance:** `[   ]`

Mixing CrossEncoder values directly with cosine redundancy is not calibrated.

#### Parent 4

**parent_key:** `DOC-008::P004::Maximal Marginal Relevance/Pipeline::8861c86de29d`

**section_path:** Maximal Marginal Relevance > Pipeline

**Parent relevance:** `[   ]`

A practical sequence is broad retrieval, CrossEncoder pruning, then dense Parent MMR.

##### Child 0

**child_key:** `DOC-008::P004::Maximal Marginal Relevance/Pipeline::8861c86de29d::C000::8861c86de29d`

**Child relevance:** `[   ]`

A practical sequence is broad retrieval, CrossEncoder pruning, then dense Parent MMR.

---

## Q015

**Query:** What happens when MMR lambda is too low?

**Query class:** MMR

**Answerability:** answerable

### Document DOC-008

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-008::P000::Maximal Marginal Relevance::fd1e2333d88d`

**section_path:** Maximal Marginal Relevance

**Parent relevance:** `[   ]`

Document ID: DOC-008

##### Child 0

**child_key:** `DOC-008::P000::Maximal Marginal Relevance::fd1e2333d88d::C000::fd1e2333d88d`

**Child relevance:** `[   ]`

Document ID: DOC-008

#### Parent 1

**parent_key:** `DOC-008::P001::Maximal Marginal Relevance/Formula::7ca32192b588`

**section_path:** Maximal Marginal Relevance > Formula

**Parent relevance:** `[   ]`

MMR balances query relevance against redundancy with already selected items. A typical objective is lambda times relevance minus one minus lambda times maximum redundancy.

##### Child 0

**child_key:** `DOC-008::P001::Maximal Marginal Relevance/Formula::7ca32192b588::C000::2cbb321f3ebb`

**Child relevance:** `[   ]`

MMR balances query relevance against redundancy with already selected items. A typical objective is lambda times

##### Child 1

**child_key:** `DOC-008::P001::Maximal Marginal Relevance/Formula::7ca32192b588::C001::d0e50a39be35`

**Child relevance:** `[   ]`

objective is lambda times relevance minus one minus lambda times maximum redundancy.

#### Parent 2

**parent_key:** `DOC-008::P002::Maximal Marginal Relevance/Lambda::b180418cbc42`

**section_path:** Maximal Marginal Relevance > Lambda

**Parent relevance:** `[   ]`

Lambda near one favors relevance. Lower lambda increases diversity, but an excessively low value may promote unusual yet weakly relevant items.

##### Child 0

**child_key:** `DOC-008::P002::Maximal Marginal Relevance/Lambda::b180418cbc42::C000::7cd845361496`

**Child relevance:** `[   ]`

Lambda near one favors relevance. Lower lambda increases diversity, but an excessively low value may promote unusual

##### Child 1

**child_key:** `DOC-008::P002::Maximal Marginal Relevance/Lambda::b180418cbc42::C001::853c1cd928a1`

**Child relevance:** `[   ]`

low value may promote unusual yet weakly relevant items.

#### Parent 3

**parent_key:** `DOC-008::P003::Maximal Marginal Relevance/Space::fab69a871cbf`

**section_path:** Maximal Marginal Relevance > Space

**Parent relevance:** `[   ]`

Dense parent MMR should compute relevance and redundancy in the same embedding space. Mixing CrossEncoder values directly with cosine redundancy is not calibrated.

##### Child 0

**child_key:** `DOC-008::P003::Maximal Marginal Relevance/Space::fab69a871cbf::C000::2801da19fbbe`

**Child relevance:** `[   ]`

Dense parent MMR should compute relevance and redundancy in the same embedding space. Mixing CrossEncoder values

##### Child 1

**child_key:** `DOC-008::P003::Maximal Marginal Relevance/Space::fab69a871cbf::C001::1dba5e9f5764`

**Child relevance:** `[   ]`

Mixing CrossEncoder values directly with cosine redundancy is not calibrated.

#### Parent 4

**parent_key:** `DOC-008::P004::Maximal Marginal Relevance/Pipeline::8861c86de29d`

**section_path:** Maximal Marginal Relevance > Pipeline

**Parent relevance:** `[   ]`

A practical sequence is broad retrieval, CrossEncoder pruning, then dense Parent MMR.

##### Child 0

**child_key:** `DOC-008::P004::Maximal Marginal Relevance/Pipeline::8861c86de29d::C000::8861c86de29d`

**Child relevance:** `[   ]`

A practical sequence is broad retrieval, CrossEncoder pruning, then dense Parent MMR.

---

## Q016

**Query:** How can headings be preserved during chunking?

**Query class:** chunking

**Answerability:** answerable

### Document DOC-009

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-009::P000::Chunking Strategies::81375c6f14b9`

**section_path:** Chunking Strategies

**Parent relevance:** `[   ]`

Document ID: DOC-009

##### Child 0

**child_key:** `DOC-009::P000::Chunking Strategies::81375c6f14b9::C000::81375c6f14b9`

**Child relevance:** `[   ]`

Document ID: DOC-009

#### Parent 1

**parent_key:** `DOC-009::P001::Chunking Strategies/Fixed::f3845b94d040`

**section_path:** Chunking Strategies > Fixed

**Parent relevance:** `[   ]`

Fixed character chunks are simple but can split semantic units. Recursive chunking tries paragraph, sentence, and whitespace boundaries before smaller fallbacks.

##### Child 0

**child_key:** `DOC-009::P001::Chunking Strategies/Fixed::f3845b94d040::C000::a68a89733877`

**Child relevance:** `[   ]`

Fixed character chunks are simple but can split semantic units. Recursive chunking tries paragraph, sentence, and

##### Child 1

**child_key:** `DOC-009::P001::Chunking Strategies/Fixed::f3845b94d040::C001::fa1c015e3d1e`

**Child relevance:** `[   ]`

tries paragraph, sentence, and whitespace boundaries before smaller fallbacks.

#### Parent 2

**parent_key:** `DOC-009::P002::Chunking Strategies/Semantic::ba2e01371136`

**section_path:** Chunking Strategies > Semantic

**Parent relevance:** `[   ]`

Semantic chunking uses embedding distance between neighboring units and can choose breakpoints from percentile, standard-deviation, IQR, or gradient rules.

##### Child 0

**child_key:** `DOC-009::P002::Chunking Strategies/Semantic::ba2e01371136::C000::ece00d9be724`

**Child relevance:** `[   ]`

Semantic chunking uses embedding distance between neighboring units and can choose breakpoints from percentile,

##### Child 1

**child_key:** `DOC-009::P002::Chunking Strategies/Semantic::ba2e01371136::C001::1219eb11380e`

**Child relevance:** `[   ]`

breakpoints from percentile, standard-deviation, IQR, or gradient rules.

#### Parent 3

**parent_key:** `DOC-009::P003::Chunking Strategies/Structure::4290d71528c6`

**section_path:** Chunking Strategies > Structure

**Parent relevance:** `[   ]`

Structure-aware chunking preserves headings, lists, code blocks, and hierarchy such as Vector Databases > HNSW > ef_construct.

##### Child 0

**child_key:** `DOC-009::P003::Chunking Strategies/Structure::4290d71528c6::C000::2983739f527c`

**Child relevance:** `[   ]`

Structure-aware chunking preserves headings, lists, code blocks, and hierarchy such as Vector Databases > HNSW >

##### Child 1

**child_key:** `DOC-009::P003::Chunking Strategies/Structure::4290d71528c6::C001::5b0b68333905`

**Child relevance:** `[   ]`

as Vector Databases > HNSW > ef_construct.

#### Parent 4

**parent_key:** `DOC-009::P004::Chunking Strategies/Evaluation::6810153bd42a`

**section_path:** Chunking Strategies > Evaluation

**Parent relevance:** `[   ]`

Chunking choices should be compared with retrieval recall, answer quality, chunk count, ingestion cost, and boundary quality.

##### Child 0

**child_key:** `DOC-009::P004::Chunking Strategies/Evaluation::6810153bd42a::C000::5f5fc84c9a3d`

**Child relevance:** `[   ]`

Chunking choices should be compared with retrieval recall, answer quality, chunk count, ingestion cost, and boundary

##### Child 1

**child_key:** `DOC-009::P004::Chunking Strategies/Evaluation::6810153bd42a::C001::4bf1bae4408c`

**Child relevance:** `[   ]`

ingestion cost, and boundary quality.

---

## Q017

**Query:** Which metadata fields are useful for filtered retrieval?

**Query class:** metadata

**Answerability:** answerable

### Document DOC-010

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-010::P000::Metadata and Filters::43e4b24991bc`

**section_path:** Metadata and Filters

**Parent relevance:** `[   ]`

Document ID: DOC-010

##### Child 0

**child_key:** `DOC-010::P000::Metadata and Filters::43e4b24991bc::C000::43e4b24991bc`

**Child relevance:** `[   ]`

Document ID: DOC-010

#### Parent 1

**parent_key:** `DOC-010::P001::Metadata and Filters/Schema::cd5fd86ef7d9`

**section_path:** Metadata and Filters > Schema

**Parent relevance:** `[   ]`

Useful metadata includes document_id, source, version, page_number, language, section_path, heading levels, content_type, tenant_id, and timestamps.

##### Child 0

**child_key:** `DOC-010::P001::Metadata and Filters/Schema::cd5fd86ef7d9::C000::db31d673e5e5`

**Child relevance:** `[   ]`

Useful metadata includes document_id, source, version, page_number, language, section_path, heading levels,

##### Child 1

**child_key:** `DOC-010::P001::Metadata and Filters/Schema::cd5fd86ef7d9::C001::0be25e8d7f99`

**Child relevance:** `[   ]`

section_path, heading levels, content_type, tenant_id, and timestamps.

#### Parent 2

**parent_key:** `DOC-010::P002::Metadata and Filters/Filtering::37575fd3a267`

**section_path:** Metadata and Filters > Filtering

**Parent relevance:** `[   ]`

Authorization fields such as tenant_id should filter before semantic ranking when cross-tenant leakage is unacceptable.

##### Child 0

**child_key:** `DOC-010::P002::Metadata and Filters/Filtering::37575fd3a267::C000::37575fd3a267`

**Child relevance:** `[   ]`

Authorization fields such as tenant_id should filter before semantic ranking when cross-tenant leakage is unacceptable.

#### Parent 3

**parent_key:** `DOC-010::P003::Metadata and Filters/Indexes::d4afdeadc68e`

**section_path:** Metadata and Filters > Indexes

**Parent relevance:** `[   ]`

Frequently filtered metadata may need payload indexes. Indexing every field wastes resources and increases write overhead.

##### Child 0

**child_key:** `DOC-010::P003::Metadata and Filters/Indexes::d4afdeadc68e::C000::3d8cce679d04`

**Child relevance:** `[   ]`

Frequently filtered metadata may need payload indexes. Indexing every field wastes resources and increases write

##### Child 1

**child_key:** `DOC-010::P003::Metadata and Filters/Indexes::d4afdeadc68e::C001::a64ddab18f12`

**Child relevance:** `[   ]`

resources and increases write overhead.

#### Parent 4

**parent_key:** `DOC-010::P004::Metadata and Filters/Debug::549b5afeb466`

**section_path:** Metadata and Filters > Debug

**Parent relevance:** `[   ]`

Document identity, parent_id, child_index, section path, and source location make retrieval results explainable.

##### Child 0

**child_key:** `DOC-010::P004::Metadata and Filters/Debug::549b5afeb466::C000::549b5afeb466`

**Child relevance:** `[   ]`

Document identity, parent_id, child_index, section path, and source location make retrieval results explainable.

---

## Q018

**Query:** Why use named dense and sparse vectors on one Qdrant point?

**Query class:** Qdrant

**Answerability:** answerable

### Document DOC-011

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-011::P000::Qdrant Named Vectors::29d39b568e2c`

**section_path:** Qdrant Named Vectors

**Parent relevance:** `[   ]`

Document ID: DOC-011

##### Child 0

**child_key:** `DOC-011::P000::Qdrant Named Vectors::29d39b568e2c::C000::29d39b568e2c`

**Child relevance:** `[   ]`

Document ID: DOC-011

#### Parent 1

**parent_key:** `DOC-011::P001::Qdrant Named Vectors/Points::64c6ee09b41d`

**section_path:** Qdrant Named Vectors > Points

**Parent relevance:** `[   ]`

A Qdrant point can contain an identifier, payload metadata, and one or more vector representations.

##### Child 0

**child_key:** `DOC-011::P001::Qdrant Named Vectors/Points::64c6ee09b41d::C000::64c6ee09b41d`

**Child relevance:** `[   ]`

A Qdrant point can contain an identifier, payload metadata, and one or more vector representations.

#### Parent 2

**parent_key:** `DOC-011::P002::Qdrant Named Vectors/Names::d4c49d146d63`

**section_path:** Qdrant Named Vectors > Names

**Parent relevance:** `[   ]`

A hybrid point can store a dense vector named dense and a sparse vector named sparse while sharing the same ChildChunk payload.

##### Child 0

**child_key:** `DOC-011::P002::Qdrant Named Vectors/Names::d4c49d146d63::C000::fa82bf2c596c`

**Child relevance:** `[   ]`

A hybrid point can store a dense vector named dense and a sparse vector named sparse while sharing the same ChildChunk

##### Child 1

**child_key:** `DOC-011::P002::Qdrant Named Vectors/Names::d4c49d146d63::C001::d2f5dd503a60`

**Child relevance:** `[   ]`

sharing the same ChildChunk payload.

#### Parent 3

**parent_key:** `DOC-011::P003::Qdrant Named Vectors/Sparse::f8e174346f22`

**section_path:** Qdrant Named Vectors > Sparse

**Parent relevance:** `[   ]`

Sparse vector indices are lexical features, not positions inside a 384-dimensional MiniLM vector.

##### Child 0

**child_key:** `DOC-011::P003::Qdrant Named Vectors/Sparse::f8e174346f22::C000::f8e174346f22`

**Child relevance:** `[   ]`

Sparse vector indices are lexical features, not positions inside a 384-dimensional MiniLM vector.

#### Parent 4

**parent_key:** `DOC-011::P004::Qdrant Named Vectors/Upsert::d3cce139ca8d`

**section_path:** Qdrant Named Vectors > Upsert

**Parent relevance:** `[   ]`

Stable point identity matters for idempotent ingestion. Recreating a collection is convenient for experiments but is not a final synchronization design.

##### Child 0

**child_key:** `DOC-011::P004::Qdrant Named Vectors/Upsert::d3cce139ca8d::C000::58e02401035c`

**Child relevance:** `[   ]`

Stable point identity matters for idempotent ingestion. Recreating a collection is convenient for experiments but is

##### Child 1

**child_key:** `DOC-011::P004::Qdrant Named Vectors/Upsert::d3cce139ca8d::C001::6b011574703b`

**Child relevance:** `[   ]`

for experiments but is not a final synchronization design.

---

## Q019

**Query:** How should unchanged Qdrant children behave on re-ingestion?

**Query class:** synchronization

**Answerability:** answerable

### Document DOC-012

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-012::P000::Qdrant Synchronization::a18f6359ba4c`

**section_path:** Qdrant Synchronization

**Parent relevance:** `[   ]`

Document ID: DOC-012

##### Child 0

**child_key:** `DOC-012::P000::Qdrant Synchronization::a18f6359ba4c::C000::a18f6359ba4c`

**Child relevance:** `[   ]`

Document ID: DOC-012

#### Parent 1

**parent_key:** `DOC-012::P001::Qdrant Synchronization/Idempotency::21e92ae60327`

**section_path:** Qdrant Synchronization > Idempotency

**Parent relevance:** `[   ]`

Repeated ingestion of unchanged source content should not create duplicate logical child points.

##### Child 0

**child_key:** `DOC-012::P001::Qdrant Synchronization/Idempotency::21e92ae60327::C000::21e92ae60327`

**Child relevance:** `[   ]`

Repeated ingestion of unchanged source content should not create duplicate logical child points.

#### Parent 2

**parent_key:** `DOC-012::P002::Qdrant Synchronization/Coarse sync::8eeba34c4f89`

**section_path:** Qdrant Synchronization > Coarse sync

**Parent relevance:** `[   ]`

Delete-all-then-reinsert synchronization is current-state correct but recomputes and rewrites unchanged vectors.

##### Child 0

**child_key:** `DOC-012::P002::Qdrant Synchronization/Coarse sync::8eeba34c4f89::C000::8eeba34c4f89`

**Child relevance:** `[   ]`

Delete-all-then-reinsert synchronization is current-state correct but recomputes and rewrites unchanged vectors.

#### Parent 3

**parent_key:** `DOC-012::P003::Qdrant Synchronization/Differential::e494d1bad168`

**section_path:** Qdrant Synchronization > Differential

**Parent relevance:** `[   ]`

Differential synchronization preserves unchanged children, inserts new or changed children, and deletes stale children. An unchanged run should approach inserted=0, unchanged=N, stale_deleted=0.

##### Child 0

**child_key:** `DOC-012::P003::Qdrant Synchronization/Differential::e494d1bad168::C000::a6be7b76f898`

**Child relevance:** `[   ]`

Differential synchronization preserves unchanged children, inserts new or changed children, and deletes stale children.

##### Child 1

**child_key:** `DOC-012::P003::Qdrant Synchronization/Differential::e494d1bad168::C001::e2aaff858b62`

**Child relevance:** `[   ]`

and deletes stale children. An unchanged run should approach inserted=0, unchanged=N, stale_deleted=0.

#### Parent 4

**parent_key:** `DOC-012::P004::Qdrant Synchronization/Dangling::a94ff5f0450e`

**section_path:** Qdrant Synchronization > Dangling

**Parent relevance:** `[   ]`

Old Qdrant children can reference parents that MongoDB no longer contains. Parent expansion should detect this integrity failure.

##### Child 0

**child_key:** `DOC-012::P004::Qdrant Synchronization/Dangling::a94ff5f0450e::C000::8a10e11f1b5b`

**Child relevance:** `[   ]`

Old Qdrant children can reference parents that MongoDB no longer contains. Parent expansion should detect this

##### Child 1

**child_key:** `DOC-012::P004::Qdrant Synchronization/Dangling::a94ff5f0450e::C001::a75bb71c1249`

**Child relevance:** `[   ]`

expansion should detect this integrity failure.

---

## Q020

**Query:** What causes MongoDB IndexOptionsConflict?

**Query class:** database error

**Answerability:** answerable

### Document DOC-013

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-013::P000::MongoDB Parent Repository::bd3b4b66f1b8`

**section_path:** MongoDB Parent Repository

**Parent relevance:** `[   ]`

Document ID: DOC-013

##### Child 0

**child_key:** `DOC-013::P000::MongoDB Parent Repository::bd3b4b66f1b8::C000::bd3b4b66f1b8`

**Child relevance:** `[   ]`

Document ID: DOC-013

#### Parent 1

**parent_key:** `DOC-013::P001::MongoDB Parent Repository/Store::fccc07403250`

**section_path:** MongoDB Parent Repository > Store

**Parent relevance:** `[   ]`

MongoDB can hold authoritative ParentChunk records while Qdrant stores searchable child representations.

##### Child 0

**child_key:** `DOC-013::P001::MongoDB Parent Repository/Store::fccc07403250::C000::fccc07403250`

**Child relevance:** `[   ]`

MongoDB can hold authoritative ParentChunk records while Qdrant stores searchable child representations.

#### Parent 2

**parent_key:** `DOC-013::P002::MongoDB Parent Repository/Indexes::22da8c0b400f`

**section_path:** MongoDB Parent Repository > Indexes

**Parent relevance:** `[   ]`

A compound unique index on document_id and content_hash can prevent duplicate logical parent content. Conflicting existing index options can produce IndexOptionsConflict.

##### Child 0

**child_key:** `DOC-013::P002::MongoDB Parent Repository/Indexes::22da8c0b400f::C000::8066d47e6e78`

**Child relevance:** `[   ]`

A compound unique index on document_id and content_hash can prevent duplicate logical parent content. Conflicting

##### Child 1

**child_key:** `DOC-013::P002::MongoDB Parent Repository/Indexes::22da8c0b400f::C001::469f1e25137b`

**Child relevance:** `[   ]`

parent content. Conflicting existing index options can produce IndexOptionsConflict.

#### Parent 3

**parent_key:** `DOC-013::P003::MongoDB Parent Repository/Sync::0f317eaa9724`

**section_path:** MongoDB Parent Repository > Sync

**Parent relevance:** `[   ]`

Parent synchronization inserts new parents, preserves unchanged persisted identifiers, and deletes stale parents based on content hashes.

##### Child 0

**child_key:** `DOC-013::P003::MongoDB Parent Repository/Sync::0f317eaa9724::C000::4d3db31af3e2`

**Child relevance:** `[   ]`

Parent synchronization inserts new parents, preserves unchanged persisted identifiers, and deletes stale parents based

##### Child 1

**child_key:** `DOC-013::P003::MongoDB Parent Repository/Sync::0f317eaa9724::C001::07ffde0db481`

**Child relevance:** `[   ]`

deletes stale parents based on content hashes.

#### Parent 4

**parent_key:** `DOC-013::P004::MongoDB Parent Repository/Lookup::78ba0de4419e`

**section_path:** MongoDB Parent Repository > Lookup

**Parent relevance:** `[   ]`

Children should be generated from persisted parents and parent expansion should fail loudly when a referenced parent is missing.

##### Child 0

**child_key:** `DOC-013::P004::MongoDB Parent Repository/Lookup::78ba0de4419e::C000::4fb647181fc1`

**Child relevance:** `[   ]`

Children should be generated from persisted parents and parent expansion should fail loudly when a referenced parent is

##### Child 1

**child_key:** `DOC-013::P004::MongoDB Parent Repository/Lookup::78ba0de4419e::C001::bfc95860d7cf`

**Child relevance:** `[   ]`

when a referenced parent is missing.

---

## Q021

**Query:** How many dimensions does all-MiniLM-L6-v2 produce?

**Query class:** exact fact

**Answerability:** answerable

### Document DOC-014

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-014::P000::Embeddings and Normalization::20a0901d7104`

**section_path:** Embeddings and Normalization

**Parent relevance:** `[   ]`

Document ID: DOC-014

##### Child 0

**child_key:** `DOC-014::P000::Embeddings and Normalization::20a0901d7104::C000::20a0901d7104`

**Child relevance:** `[   ]`

Document ID: DOC-014

#### Parent 1

**parent_key:** `DOC-014::P001::Embeddings and Normalization/Model::07c2e4da65c0`

**section_path:** Embeddings and Normalization > Model

**Parent relevance:** `[   ]`

all-MiniLM-L6-v2 is a lightweight sentence-transformer baseline that produces 384-dimensional dense embeddings.

##### Child 0

**child_key:** `DOC-014::P001::Embeddings and Normalization/Model::07c2e4da65c0::C000::07c2e4da65c0`

**Child relevance:** `[   ]`

all-MiniLM-L6-v2 is a lightweight sentence-transformer baseline that produces 384-dimensional dense embeddings.

#### Parent 2

**parent_key:** `DOC-014::P002::Embeddings and Normalization/Normalize::1309eb85b7ae`

**section_path:** Embeddings and Normalization > Normalize

**Parent relevance:** `[   ]`

Unit-normalized vectors make cosine similarity equivalent to dot product. Query and document preprocessing should be consistent.

##### Child 0

**child_key:** `DOC-014::P002::Embeddings and Normalization/Normalize::1309eb85b7ae::C000::6e42a52ec781`

**Child relevance:** `[   ]`

Unit-normalized vectors make cosine similarity equivalent to dot product. Query and document preprocessing should be

##### Child 1

**child_key:** `DOC-014::P002::Embeddings and Normalization/Normalize::1309eb85b7ae::C001::0fc000512ac8`

**Child relevance:** `[   ]`

preprocessing should be consistent.

#### Parent 3

**parent_key:** `DOC-014::P003::Embeddings and Normalization/Migration::8c65cdc01b1f`

**section_path:** Embeddings and Normalization > Migration

**Parent relevance:** `[   ]`

Changing to a model with another dimensionality requires regenerating vectors and using a compatible collection configuration.

##### Child 0

**child_key:** `DOC-014::P003::Embeddings and Normalization/Migration::8c65cdc01b1f::C000::f71912382f85`

**Child relevance:** `[   ]`

Changing to a model with another dimensionality requires regenerating vectors and using a compatible collection

##### Child 1

**child_key:** `DOC-014::P003::Embeddings and Normalization/Migration::8c65cdc01b1f::C001::e10be5b0cc8f`

**Child relevance:** `[   ]`

using a compatible collection configuration.

#### Parent 4

**parent_key:** `DOC-014::P004::Embeddings and Normalization/Domain::328e60d2cbe2`

**section_path:** Embeddings and Normalization > Domain

**Parent relevance:** `[   ]`

Generic semantic quality does not guarantee strong handling of product identifiers, uncommon acronyms, or error strings.

##### Child 0

**child_key:** `DOC-014::P004::Embeddings and Normalization/Domain::328e60d2cbe2::C000::328e60d2cbe2`

**Child relevance:** `[   ]`

Generic semantic quality does not guarantee strong handling of product identifiers, uncommon acronyms, or error strings.

---

## Q022

**Query:** What problem does query rewriting solve?

**Query class:** advanced retrieval

**Answerability:** answerable

### Document DOC-015

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-015::P000::Query Rewriting::06ca3d4e7c02`

**section_path:** Query Rewriting

**Parent relevance:** `[   ]`

Document ID: DOC-015

##### Child 0

**child_key:** `DOC-015::P000::Query Rewriting::06ca3d4e7c02::C000::06ca3d4e7c02`

**Child relevance:** `[   ]`

Document ID: DOC-015

#### Parent 1

**parent_key:** `DOC-015::P001::Query Rewriting/Purpose::d56f777bf8e0`

**section_path:** Query Rewriting > Purpose

**Parent relevance:** `[   ]`

Query rewriting changes wording to better match corpus terminology while trying to preserve the original intent.

##### Child 0

**child_key:** `DOC-015::P001::Query Rewriting/Purpose::d56f777bf8e0::C000::d56f777bf8e0`

**Child relevance:** `[   ]`

Query rewriting changes wording to better match corpus terminology while trying to preserve the original intent.

#### Parent 2

**parent_key:** `DOC-015::P002::Query Rewriting/Example::2c81dc401950`

**section_path:** Query Rewriting > Example

**Parent relevance:** `[   ]`

How does HNSW search efficiently can be rewritten toward graph traversal, upper-to-lower layers, and avoiding comparison with every vector.

##### Child 0

**child_key:** `DOC-015::P002::Query Rewriting/Example::2c81dc401950::C000::cf6ef35fbab8`

**Child relevance:** `[   ]`

How does HNSW search efficiently can be rewritten toward graph traversal, upper-to-lower layers, and avoiding

##### Child 1

**child_key:** `DOC-015::P002::Query Rewriting/Example::2c81dc401950::C001::af36cd09845e`

**Child relevance:** `[   ]`

layers, and avoiding comparison with every vector.

#### Parent 3

**parent_key:** `DOC-015::P003::Query Rewriting/Risk::da1cc5a797de`

**section_path:** Query Rewriting > Risk

**Parent relevance:** `[   ]`

A rewriter can introduce assumptions or drift. Systems should retain the original query and may retrieve with both forms.

##### Child 0

**child_key:** `DOC-015::P003::Query Rewriting/Risk::da1cc5a797de::C000::a7b12c5eb691`

**Child relevance:** `[   ]`

A rewriter can introduce assumptions or drift. Systems should retain the original query and may retrieve with both

##### Child 1

**child_key:** `DOC-015::P003::Query Rewriting/Risk::da1cc5a797de::C001::dfc34ec49d76`

**Child relevance:** `[   ]`

and may retrieve with both forms.

#### Parent 4

**parent_key:** `DOC-015::P004::Query Rewriting/Measure::07c6a54bef3e`

**section_path:** Query Rewriting > Measure

**Parent relevance:** `[   ]`

Judge rewriting with downstream retrieval metrics rather than linguistic elegance.

##### Child 0

**child_key:** `DOC-015::P004::Query Rewriting/Measure::07c6a54bef3e::C000::07c6a54bef3e`

**Child relevance:** `[   ]`

Judge rewriting with downstream retrieval metrics rather than linguistic elegance.

---

## Q023

**Query:** Why can multi-query retrieval improve recall?

**Query class:** advanced retrieval

**Answerability:** answerable

### Document DOC-016

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-016::P000::Multi Query Retrieval::d38a33f2bbb7`

**section_path:** Multi Query Retrieval

**Parent relevance:** `[   ]`

Document ID: DOC-016

##### Child 0

**child_key:** `DOC-016::P000::Multi Query Retrieval::d38a33f2bbb7::C000::d38a33f2bbb7`

**Child relevance:** `[   ]`

Document ID: DOC-016

#### Parent 1

**parent_key:** `DOC-016::P001::Multi Query Retrieval/Views::4cecdf1699ce`

**section_path:** Multi Query Retrieval > Views

**Parent relevance:** `[   ]`

Multi-query retrieval generates several search formulations from one user request, retrieves for each, then merges and deduplicates candidates.

##### Child 0

**child_key:** `DOC-016::P001::Multi Query Retrieval/Views::4cecdf1699ce::C000::ff1c6d2021ab`

**Child relevance:** `[   ]`

Multi-query retrieval generates several search formulations from one user request, retrieves for each, then merges and

##### Child 1

**child_key:** `DOC-016::P001::Multi Query Retrieval/Views::4cecdf1699ce::C001::26b4297c7d02`

**Child relevance:** `[   ]`

for each, then merges and deduplicates candidates.

#### Parent 2

**parent_key:** `DOC-016::P002::Multi Query Retrieval/Recall::353efadcdd3a`

**section_path:** Multi Query Retrieval > Recall

**Parent relevance:** `[   ]`

Different phrasings can recover evidence using terms such as graph traversal, approximate neighbors, upper layers, or search frontier.

##### Child 0

**child_key:** `DOC-016::P002::Multi Query Retrieval/Recall::353efadcdd3a::C000::acd317bf3628`

**Child relevance:** `[   ]`

Different phrasings can recover evidence using terms such as graph traversal, approximate neighbors, upper layers, or

##### Child 1

**child_key:** `DOC-016::P002::Multi Query Retrieval/Recall::353efadcdd3a::C001::5eb263431949`

**Child relevance:** `[   ]`

neighbors, upper layers, or search frontier.

#### Parent 3

**parent_key:** `DOC-016::P003::Multi Query Retrieval/Cost::9c9e422e820a`

**section_path:** Multi Query Retrieval > Cost

**Parent relevance:** `[   ]`

Every generated query adds embedding, vector search, sparse search, and possibly reranking work.

##### Child 0

**child_key:** `DOC-016::P003::Multi Query Retrieval/Cost::9c9e422e820a::C000::9c9e422e820a`

**Child relevance:** `[   ]`

Every generated query adds embedding, vector search, sparse search, and possibly reranking work.

#### Parent 4

**parent_key:** `DOC-016::P004::Multi Query Retrieval/Fusion::c89738d0a058`

**section_path:** Multi Query Retrieval > Fusion

**Parent relevance:** `[   ]`

Multi-query results can be merged with rank fusion, maximum score, or another rule; noisy generated queries can otherwise promote distractors.

##### Child 0

**child_key:** `DOC-016::P004::Multi Query Retrieval/Fusion::c89738d0a058::C000::696a3bfbb4f1`

**Child relevance:** `[   ]`

Multi-query results can be merged with rank fusion, maximum score, or another rule; noisy generated queries can

##### Child 1

**child_key:** `DOC-016::P004::Multi Query Retrieval/Fusion::c89738d0a058::C001::4a9393588762`

**Child relevance:** `[   ]`

noisy generated queries can otherwise promote distractors.

---

## Q024

**Query:** What is HyDE and why can it hallucinate?

**Query class:** advanced retrieval

**Answerability:** answerable

### Document DOC-017

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-017::P000::HyDE::c7ddae71dc0e`

**section_path:** HyDE

**Parent relevance:** `[   ]`

Document ID: DOC-017

##### Child 0

**child_key:** `DOC-017::P000::HyDE::c7ddae71dc0e::C000::c7ddae71dc0e`

**Child relevance:** `[   ]`

Document ID: DOC-017

#### Parent 1

**parent_key:** `DOC-017::P001::HyDE/Idea::65b4780365ac`

**section_path:** HyDE > Idea

**Parent relevance:** `[   ]`

Hypothetical Document Embeddings generate an answer-like hypothetical passage, embed it, and use that embedding for retrieval.

##### Child 0

**child_key:** `DOC-017::P001::HyDE/Idea::65b4780365ac::C000::5d1d934f89b6`

**Child relevance:** `[   ]`

Hypothetical Document Embeddings generate an answer-like hypothetical passage, embed it, and use that embedding for

##### Child 1

**child_key:** `DOC-017::P001::HyDE/Idea::65b4780365ac::C001::cf816d58fd75`

**Child relevance:** `[   ]`

it, and use that embedding for retrieval.

#### Parent 2

**parent_key:** `DOC-017::P002::HyDE/Bridge::a4b3d568eb10`

**section_path:** HyDE > Bridge

**Parent relevance:** `[   ]`

The hypothetical passage may introduce terminology closer to the corpus than the original short question.

##### Child 0

**child_key:** `DOC-017::P002::HyDE/Bridge::a4b3d568eb10::C000::a4b3d568eb10`

**Child relevance:** `[   ]`

The hypothetical passage may introduce terminology closer to the corpus than the original short question.

#### Parent 3

**parent_key:** `DOC-017::P003::HyDE/Risk::ae3207221e80`

**section_path:** HyDE > Risk

**Parent relevance:** `[   ]`

The hypothetical document may hallucinate. It is only a retrieval aid and must never replace source evidence.

##### Child 0

**child_key:** `DOC-017::P003::HyDE/Risk::ae3207221e80::C000::ae3207221e80`

**Child relevance:** `[   ]`

The hypothetical document may hallucinate. It is only a retrieval aid and must never replace source evidence.

#### Parent 4

**parent_key:** `DOC-017::P004::HyDE/Measure::88b7f6851191`

**section_path:** HyDE > Measure

**Parent relevance:** `[   ]`

Compare HyDE against original-query retrieval because its extra generation step adds cost and is not universally beneficial.

##### Child 0

**child_key:** `DOC-017::P004::HyDE/Measure::88b7f6851191::C000::5bd621c60ff1`

**Child relevance:** `[   ]`

Compare HyDE against original-query retrieval because its extra generation step adds cost and is not universally

##### Child 1

**child_key:** `DOC-017::P004::HyDE/Measure::88b7f6851191::C001::097ccdca11e4`

**Child relevance:** `[   ]`

cost and is not universally beneficial.

---

## Q025

**Query:** What is candidate parent recall?

**Query class:** evaluation

**Answerability:** answerable

### Document DOC-018

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-018::P000::RAG Evaluation::fac04aa39b28`

**section_path:** RAG Evaluation

**Parent relevance:** `[   ]`

Document ID: DOC-018

##### Child 0

**child_key:** `DOC-018::P000::RAG Evaluation::fac04aa39b28::C000::fac04aa39b28`

**Child relevance:** `[   ]`

Document ID: DOC-018

#### Parent 1

**parent_key:** `DOC-018::P001::RAG Evaluation/Metrics::c46eea5d9f13`

**section_path:** RAG Evaluation > Metrics

**Parent relevance:** `[   ]`

Hit Rate checks whether a relevant item appears in top K. Recall@K measures coverage of known relevant items. Mean Reciprocal Rank rewards placing the first relevant item near the top.

##### Child 0

**child_key:** `DOC-018::P001::RAG Evaluation/Metrics::c46eea5d9f13::C000::d28a36e53577`

**Child relevance:** `[   ]`

Hit Rate checks whether a relevant item appears in top K. Recall@K measures coverage of known relevant items. Mean

##### Child 1

**child_key:** `DOC-018::P001::RAG Evaluation/Metrics::c46eea5d9f13::C001::8d9281b35d56`

**Child relevance:** `[   ]`

of known relevant items. Mean Reciprocal Rank rewards placing the first relevant item near the top.

#### Parent 2

**parent_key:** `DOC-018::P002::RAG Evaluation/Parents::38fe5954a8bf`

**section_path:** RAG Evaluation > Parents

**Parent relevance:** `[   ]`

Child recall and parent recall differ because several child hits may collapse to one parent. Candidate parent recall before reranking is especially important.

##### Child 0

**child_key:** `DOC-018::P002::RAG Evaluation/Parents::38fe5954a8bf::C000::19cfc0526d27`

**Child relevance:** `[   ]`

Child recall and parent recall differ because several child hits may collapse to one parent. Candidate parent recall

##### Child 1

**child_key:** `DOC-018::P002::RAG Evaluation/Parents::38fe5954a8bf::C001::99550e8ff68c`

**Child relevance:** `[   ]`

Candidate parent recall before reranking is especially important.

#### Parent 3

**parent_key:** `DOC-018::P003::RAG Evaluation/Answer::1b0b32e5b5b6`

**section_path:** RAG Evaluation > Answer

**Parent relevance:** `[   ]`

Retrieval metrics do not fully determine answer quality. Faithfulness, answer relevance, context precision, and citation correctness are separate concerns.

##### Child 0

**child_key:** `DOC-018::P003::RAG Evaluation/Answer::1b0b32e5b5b6::C000::7f1f3d5022cf`

**Child relevance:** `[   ]`

Retrieval metrics do not fully determine answer quality. Faithfulness, answer relevance, context precision, and

##### Child 1

**child_key:** `DOC-018::P003::RAG Evaluation/Answer::1b0b32e5b5b6::C001::ab7cb10bace2`

**Child relevance:** `[   ]`

context precision, and citation correctness are separate concerns.

#### Parent 4

**parent_key:** `DOC-018::P004::RAG Evaluation/Gold::b653a61ef392`

**section_path:** RAG Evaluation > Gold

**Parent relevance:** `[   ]`

A golden benchmark should include exact identifiers, semantic paraphrases, ambiguous questions, multi-section needs, and unanswerable queries.

##### Child 0

**child_key:** `DOC-018::P004::RAG Evaluation/Gold::b653a61ef392::C000::fe46b40ac0c9`

**Child relevance:** `[   ]`

A golden benchmark should include exact identifiers, semantic paraphrases, ambiguous questions, multi-section needs,

##### Child 1

**child_key:** `DOC-018::P004::RAG Evaluation/Gold::b653a61ef392::C001::581d360a5038`

**Child relevance:** `[   ]`

multi-section needs, and unanswerable queries.

---

## Q026

**Query:** Why is FastAPI returning HTTP 422?

**Query class:** exact error

**Answerability:** answerable

### Document DOC-019

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-019::P000::FastAPI RAG Services::03f46338a01e`

**section_path:** FastAPI RAG Services

**Parent relevance:** `[   ]`

Document ID: DOC-019

##### Child 0

**child_key:** `DOC-019::P000::FastAPI RAG Services::03f46338a01e::C000::03f46338a01e`

**Child relevance:** `[   ]`

Document ID: DOC-019

#### Parent 1

**parent_key:** `DOC-019::P001::FastAPI RAG Services/API::5862539c5adb`

**section_path:** FastAPI RAG Services > API

**Parent relevance:** `[   ]`

A RAG service may expose POST /query, POST /ingest, GET /health, and document endpoints using Pydantic request and response models.

##### Child 0

**child_key:** `DOC-019::P001::FastAPI RAG Services/API::5862539c5adb::C000::4f760e77c6a7`

**Child relevance:** `[   ]`

A RAG service may expose POST /query, POST /ingest, GET /health, and document endpoints using Pydantic request and

##### Child 1

**child_key:** `DOC-019::P001::FastAPI RAG Services/API::5862539c5adb::C001::05ec4a18837c`

**Child relevance:** `[   ]`

using Pydantic request and response models.

#### Parent 2

**parent_key:** `DOC-019::P002::FastAPI RAG Services/HTTP 422::c9c8bfaad7e3`

**section_path:** FastAPI RAG Services > HTTP 422

**Parent relevance:** `[   ]`

FastAPI commonly returns HTTP 422 when request data fails validation against the declared schema. This is an API validation failure, not a retrieval-quality failure.

##### Child 0

**child_key:** `DOC-019::P002::FastAPI RAG Services/HTTP 422::c9c8bfaad7e3::C000::0ce1bba56b88`

**Child relevance:** `[   ]`

FastAPI commonly returns HTTP 422 when request data fails validation against the declared schema. This is an API

##### Child 1

**child_key:** `DOC-019::P002::FastAPI RAG Services/HTTP 422::c9c8bfaad7e3::C001::684f40fbdb0f`

**Child relevance:** `[   ]`

schema. This is an API validation failure, not a retrieval-quality failure.

#### Parent 3

**parent_key:** `DOC-019::P003::FastAPI RAG Services/Boundaries::b9106e81f54b`

**section_path:** FastAPI RAG Services > Boundaries

**Parent relevance:** `[   ]`

Embedding services, repositories, vector stores, retrievers, and rerankers should be initialized through clear application boundaries.

##### Child 0

**child_key:** `DOC-019::P003::FastAPI RAG Services/Boundaries::b9106e81f54b::C000::cb4a34cacc86`

**Child relevance:** `[   ]`

Embedding services, repositories, vector stores, retrievers, and rerankers should be initialized through clear

##### Child 1

**child_key:** `DOC-019::P003::FastAPI RAG Services/Boundaries::b9106e81f54b::C001::908886a5b5d0`

**Child relevance:** `[   ]`

be initialized through clear application boundaries.

#### Parent 4

**parent_key:** `DOC-019::P004::FastAPI RAG Services/Trace::7758ad0c2671`

**section_path:** FastAPI RAG Services > Trace

**Parent relevance:** `[   ]`

Request IDs, retrieval timings, candidate counts, and final document IDs are useful production signals.

##### Child 0

**child_key:** `DOC-019::P004::FastAPI RAG Services/Trace::7758ad0c2671::C000::7758ad0c2671`

**Child relevance:** `[   ]`

Request IDs, retrieval timings, candidate counts, and final document IDs are useful production signals.

---

## Q027

**Query:** What can cause ERR_CONNECTION_REFUSED?

**Query class:** exact error

**Answerability:** answerable

### Document DOC-020

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-020::P000::Docker and Local Infrastructure::8e4d923a0898`

**section_path:** Docker and Local Infrastructure

**Parent relevance:** `[   ]`

Document ID: DOC-020

##### Child 0

**child_key:** `DOC-020::P000::Docker and Local Infrastructure::8e4d923a0898::C000::8e4d923a0898`

**Child relevance:** `[   ]`

Document ID: DOC-020

#### Parent 1

**parent_key:** `DOC-020::P001::Docker and Local Infrastructure/Services::ca0ff7cff8a1`

**section_path:** Docker and Local Infrastructure > Services

**Parent relevance:** `[   ]`

A local stack can run Qdrant, MongoDB, and the Python API as separate services with explicit ports and health checks.

##### Child 0

**child_key:** `DOC-020::P001::Docker and Local Infrastructure/Services::ca0ff7cff8a1::C000::ca0ff7cff8a1`

**Child relevance:** `[   ]`

A local stack can run Qdrant, MongoDB, and the Python API as separate services with explicit ports and health checks.

#### Parent 2

**parent_key:** `DOC-020::P002::Docker and Local Infrastructure/Refused::363edf91f09a`

**section_path:** Docker and Local Infrastructure > Refused

**Parent relevance:** `[   ]`

ERR_CONNECTION_REFUSED usually means the target service is not listening, a container is stopped, the host or port is wrong, or networking is misconfigured.

##### Child 0

**child_key:** `DOC-020::P002::Docker and Local Infrastructure/Refused::363edf91f09a::C000::fa3330ad34e9`

**Child relevance:** `[   ]`

ERR_CONNECTION_REFUSED usually means the target service is not listening, a container is stopped, the host or port is

##### Child 1

**child_key:** `DOC-020::P002::Docker and Local Infrastructure/Refused::363edf91f09a::C001::f8fe90ce9d24`

**Child relevance:** `[   ]`

stopped, the host or port is wrong, or networking is misconfigured.

#### Parent 3

**parent_key:** `DOC-020::P003::Docker and Local Infrastructure/Persistence::e7b5069e8ff8`

**section_path:** Docker and Local Infrastructure > Persistence

**Parent relevance:** `[   ]`

Persistent volumes preserve Qdrant and MongoDB data across container recreation.

##### Child 0

**child_key:** `DOC-020::P003::Docker and Local Infrastructure/Persistence::e7b5069e8ff8::C000::e7b5069e8ff8`

**Child relevance:** `[   ]`

Persistent volumes preserve Qdrant and MongoDB data across container recreation.

#### Parent 4

**parent_key:** `DOC-020::P004::Docker and Local Infrastructure/Config::48b1c4564012`

**section_path:** Docker and Local Infrastructure > Config

**Parent relevance:** `[   ]`

Environment variables should hold service URLs and credentials while local defaults may use http://localhost:6333 for Qdrant.

##### Child 0

**child_key:** `DOC-020::P004::Docker and Local Infrastructure/Config::48b1c4564012::C000::dcdedc79b0b7`

**Child relevance:** `[   ]`

Environment variables should hold service URLs and credentials while local defaults may use http://localhost:6333 for

##### Child 1

**child_key:** `DOC-020::P004::Docker and Local Infrastructure/Config::48b1c4564012::C001::77191a03fadc`

**Child relevance:** `[   ]`

use http://localhost:6333 for Qdrant.

---

## Q028

**Query:** How should I trace dense sparse RRF CrossEncoder and MMR scores?

**Query class:** observability

**Answerability:** answerable

### Document DOC-021

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-021::P000::Retrieval Observability::969b9acbc014`

**section_path:** Retrieval Observability

**Parent relevance:** `[   ]`

Document ID: DOC-021

##### Child 0

**child_key:** `DOC-021::P000::Retrieval Observability::969b9acbc014::C000::969b9acbc014`

**Child relevance:** `[   ]`

Document ID: DOC-021

#### Parent 1

**parent_key:** `DOC-021::P001::Retrieval Observability/Stages::f0aab813c305`

**section_path:** Retrieval Observability > Stages

**Parent relevance:** `[   ]`

Trace dense, sparse, RRF fusion, parent expansion, CrossEncoder, MMR, and final context separately.

##### Child 0

**child_key:** `DOC-021::P001::Retrieval Observability/Stages::f0aab813c305::C000::f0aab813c305`

**Child relevance:** `[   ]`

Trace dense, sparse, RRF fusion, parent expansion, CrossEncoder, MMR, and final context separately.

#### Parent 2

**parent_key:** `DOC-021::P002::Retrieval Observability/Scores::850158a138ab`

**section_path:** Retrieval Observability > Scores

**Parent relevance:** `[   ]`

An RRF score, cosine similarity, BM25 score, and CrossEncoder output have different meanings and should not be logged under an unlabeled generic score.

##### Child 0

**child_key:** `DOC-021::P002::Retrieval Observability/Scores::850158a138ab::C000::357f6c5794b1`

**Child relevance:** `[   ]`

An RRF score, cosine similarity, BM25 score, and CrossEncoder output have different meanings and should not be logged

##### Child 1

**child_key:** `DOC-021::P002::Retrieval Observability/Scores::850158a138ab::C001::c795f418b739`

**Child relevance:** `[   ]`

and should not be logged under an unlabeled generic score.

#### Parent 3

**parent_key:** `DOC-021::P003::Retrieval Observability/Latency::713b3e62ea2e`

**section_path:** Retrieval Observability > Latency

**Parent relevance:** `[   ]`

Measure embedding, dense search, sparse search, fusion, MongoDB lookup, reranker inference, and MMR latency separately.

##### Child 0

**child_key:** `DOC-021::P003::Retrieval Observability/Latency::713b3e62ea2e::C000::713b3e62ea2e`

**Child relevance:** `[   ]`

Measure embedding, dense search, sparse search, fusion, MongoDB lookup, reranker inference, and MMR latency separately.

#### Parent 4

**parent_key:** `DOC-021::P004::Retrieval Observability/Diagnosis::3d5ab9d780a5`

**section_path:** Retrieval Observability > Diagnosis

**Parent relevance:** `[   ]`

Stage-level traces reveal whether bad answers came from candidate recall, stale parent links, reranking, diversity selection, or generation.

##### Child 0

**child_key:** `DOC-021::P004::Retrieval Observability/Diagnosis::3d5ab9d780a5::C000::8f479040a451`

**Child relevance:** `[   ]`

Stage-level traces reveal whether bad answers came from candidate recall, stale parent links, reranking, diversity

##### Child 1

**child_key:** `DOC-021::P004::Retrieval Observability/Diagnosis::3d5ab9d780a5::C001::a2e44798d6cc`

**Child relevance:** `[   ]`

links, reranking, diversity selection, or generation.

---

## Q029

**Query:** Can similarity override tenant_id authorization?

**Query class:** security

**Answerability:** answerable

### Document DOC-022

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-022::P000::Tenant Isolation::51bac1b9098f`

**section_path:** Tenant Isolation

**Parent relevance:** `[   ]`

Document ID: DOC-022

##### Child 0

**child_key:** `DOC-022::P000::Tenant Isolation::51bac1b9098f::C000::51bac1b9098f`

**Child relevance:** `[   ]`

Document ID: DOC-022

#### Parent 1

**parent_key:** `DOC-022::P001::Tenant Isolation/Tenant::c1eeb5577192`

**section_path:** Tenant Isolation > Tenant

**Parent relevance:** `[   ]`

tenant_id should be a retrieval constraint when tenants must not access one another's documents.

##### Child 0

**child_key:** `DOC-022::P001::Tenant Isolation/Tenant::c1eeb5577192::C000::c1eeb5577192`

**Child relevance:** `[   ]`

tenant_id should be a retrieval constraint when tenants must not access one another's documents.

#### Parent 2

**parent_key:** `DOC-022::P002::Tenant Isolation/Permissions::e763650ac01e`

**section_path:** Tenant Isolation > Permissions

**Parent relevance:** `[   ]`

Access rules may also use source_id, project_id, category, or group metadata with consistent types and index support.

##### Child 0

**child_key:** `DOC-022::P002::Tenant Isolation/Permissions::e763650ac01e::C000::e763650ac01e`

**Child relevance:** `[   ]`

Access rules may also use source_id, project_id, category, or group metadata with consistent types and index support.

#### Parent 3

**parent_key:** `DOC-022::P003::Tenant Isolation/Security::5f74c2b044e0`

**section_path:** Tenant Isolation > Security

**Parent relevance:** `[   ]`

Semantic relevance can never override authorization. Permission filtering and retrieval ranking solve different problems.

##### Child 0

**child_key:** `DOC-022::P003::Tenant Isolation/Security::5f74c2b044e0::C000::e30156b5d141`

**Child relevance:** `[   ]`

Semantic relevance can never override authorization. Permission filtering and retrieval ranking solve different

##### Child 1

**child_key:** `DOC-022::P003::Tenant Isolation/Security::5f74c2b044e0::C001::cc19f8f1e3bb`

**Child relevance:** `[   ]`

ranking solve different problems.

#### Parent 4

**parent_key:** `DOC-022::P004::Tenant Isolation/Test::fe81f4b0c023`

**section_path:** Tenant Isolation > Test

**Parent relevance:** `[   ]`

Negative tests should prove that tenant A cannot retrieve tenant B content even if their text is nearly identical.

##### Child 0

**child_key:** `DOC-022::P004::Tenant Isolation/Test::fe81f4b0c023::C000::fe81f4b0c023`

**Child relevance:** `[   ]`

Negative tests should prove that tenant A cannot retrieve tenant B content even if their text is nearly identical.

---

## Q030

**Query:** What causes a vector dimension mismatch?

**Query class:** failure mode

**Answerability:** answerable

### Document DOC-023

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-023::P000::Vector Search Failure Modes::ff3515e2f802`

**section_path:** Vector Search Failure Modes

**Parent relevance:** `[   ]`

Document ID: DOC-023

##### Child 0

**child_key:** `DOC-023::P000::Vector Search Failure Modes::ff3515e2f802::C000::ff3515e2f802`

**Child relevance:** `[   ]`

Document ID: DOC-023

#### Parent 1

**parent_key:** `DOC-023::P001::Vector Search Failure Modes/Dimensions::efac2cf482ff`

**section_path:** Vector Search Failure Modes > Dimensions

**Parent relevance:** `[   ]`

A collection configured for 384-dimensional vectors cannot accept 768-dimensional vectors. Model migrations often expose this error.

##### Child 0

**child_key:** `DOC-023::P001::Vector Search Failure Modes/Dimensions::efac2cf482ff::C000::697456d2070e`

**Child relevance:** `[   ]`

A collection configured for 384-dimensional vectors cannot accept 768-dimensional vectors. Model migrations often

##### Child 1

**child_key:** `DOC-023::P001::Vector Search Failure Modes/Dimensions::efac2cf482ff::C001::95572a61f3da`

**Child relevance:** `[   ]`

Model migrations often expose this error.

#### Parent 2

**parent_key:** `DOC-023::P002::Vector Search Failure Modes/Duplicates::bf76d5a4fc0b`

**section_path:** Vector Search Failure Modes > Duplicates

**Parent relevance:** `[   ]`

Repeated ingestion creates duplicates if logical chunks receive new random point identities and no synchronization reconciles them.

##### Child 0

**child_key:** `DOC-023::P002::Vector Search Failure Modes/Duplicates::bf76d5a4fc0b::C000::6f015e9cbf16`

**Child relevance:** `[   ]`

Repeated ingestion creates duplicates if logical chunks receive new random point identities and no synchronization

##### Child 1

**child_key:** `DOC-023::P002::Vector Search Failure Modes/Duplicates::bf76d5a4fc0b::C001::7e02b8d3492d`

**Child relevance:** `[   ]`

and no synchronization reconciles them.

#### Parent 3

**parent_key:** `DOC-023::P003::Vector Search Failure Modes/Recall::44cf3f50eabc`

**section_path:** Vector Search Failure Modes > Recall

**Parent relevance:** `[   ]`

Low recall can result from poor chunking, weak embeddings, small candidate pools, restrictive filters, HNSW settings, or missing source content.

##### Child 0

**child_key:** `DOC-023::P003::Vector Search Failure Modes/Recall::44cf3f50eabc::C000::83e8e58842a4`

**Child relevance:** `[   ]`

Low recall can result from poor chunking, weak embeddings, small candidate pools, restrictive filters, HNSW settings,

##### Child 1

**child_key:** `DOC-023::P003::Vector Search Failure Modes/Recall::44cf3f50eabc::C001::3c3b4f503a50`

**Child relevance:** `[   ]`

filters, HNSW settings, or missing source content.

#### Parent 4

**parent_key:** `DOC-023::P004::Vector Search Failure Modes/Scores::2b32cd5bfec4`

**section_path:** Vector Search Failure Modes > Scores

**Parent relevance:** `[   ]`

High cosine similarity means semantic relatedness, not guaranteed answer correctness; low CrossEncoder output may also reflect query phrasing.

##### Child 0

**child_key:** `DOC-023::P004::Vector Search Failure Modes/Scores::2b32cd5bfec4::C000::232fb5ae9d65`

**Child relevance:** `[   ]`

High cosine similarity means semantic relatedness, not guaranteed answer correctness; low CrossEncoder output may also

##### Child 1

**child_key:** `DOC-023::P004::Vector Search Failure Modes/Scores::2b32cd5bfec4::C001::d595f20942e6`

**Child relevance:** `[   ]`

CrossEncoder output may also reflect query phrasing.

### Document DOC-014

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-014::P000::Embeddings and Normalization::20a0901d7104`

**section_path:** Embeddings and Normalization

**Parent relevance:** `[   ]`

Document ID: DOC-014

##### Child 0

**child_key:** `DOC-014::P000::Embeddings and Normalization::20a0901d7104::C000::20a0901d7104`

**Child relevance:** `[   ]`

Document ID: DOC-014

#### Parent 1

**parent_key:** `DOC-014::P001::Embeddings and Normalization/Model::07c2e4da65c0`

**section_path:** Embeddings and Normalization > Model

**Parent relevance:** `[   ]`

all-MiniLM-L6-v2 is a lightweight sentence-transformer baseline that produces 384-dimensional dense embeddings.

##### Child 0

**child_key:** `DOC-014::P001::Embeddings and Normalization/Model::07c2e4da65c0::C000::07c2e4da65c0`

**Child relevance:** `[   ]`

all-MiniLM-L6-v2 is a lightweight sentence-transformer baseline that produces 384-dimensional dense embeddings.

#### Parent 2

**parent_key:** `DOC-014::P002::Embeddings and Normalization/Normalize::1309eb85b7ae`

**section_path:** Embeddings and Normalization > Normalize

**Parent relevance:** `[   ]`

Unit-normalized vectors make cosine similarity equivalent to dot product. Query and document preprocessing should be consistent.

##### Child 0

**child_key:** `DOC-014::P002::Embeddings and Normalization/Normalize::1309eb85b7ae::C000::6e42a52ec781`

**Child relevance:** `[   ]`

Unit-normalized vectors make cosine similarity equivalent to dot product. Query and document preprocessing should be

##### Child 1

**child_key:** `DOC-014::P002::Embeddings and Normalization/Normalize::1309eb85b7ae::C001::0fc000512ac8`

**Child relevance:** `[   ]`

preprocessing should be consistent.

#### Parent 3

**parent_key:** `DOC-014::P003::Embeddings and Normalization/Migration::8c65cdc01b1f`

**section_path:** Embeddings and Normalization > Migration

**Parent relevance:** `[   ]`

Changing to a model with another dimensionality requires regenerating vectors and using a compatible collection configuration.

##### Child 0

**child_key:** `DOC-014::P003::Embeddings and Normalization/Migration::8c65cdc01b1f::C000::f71912382f85`

**Child relevance:** `[   ]`

Changing to a model with another dimensionality requires regenerating vectors and using a compatible collection

##### Child 1

**child_key:** `DOC-014::P003::Embeddings and Normalization/Migration::8c65cdc01b1f::C001::e10be5b0cc8f`

**Child relevance:** `[   ]`

using a compatible collection configuration.

#### Parent 4

**parent_key:** `DOC-014::P004::Embeddings and Normalization/Domain::328e60d2cbe2`

**section_path:** Embeddings and Normalization > Domain

**Parent relevance:** `[   ]`

Generic semantic quality does not guarantee strong handling of product identifiers, uncommon acronyms, or error strings.

##### Child 0

**child_key:** `DOC-014::P004::Embeddings and Normalization/Domain::328e60d2cbe2::C000::328e60d2cbe2`

**Child relevance:** `[   ]`

Generic semantic quality does not guarantee strong handling of product identifiers, uncommon acronyms, or error strings.

---

## Q031

**Query:** Which metrics should compare Dense Sparse and Hybrid?

**Query class:** evaluation

**Answerability:** answerable

### Document DOC-018

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-018::P000::RAG Evaluation::fac04aa39b28`

**section_path:** RAG Evaluation

**Parent relevance:** `[   ]`

Document ID: DOC-018

##### Child 0

**child_key:** `DOC-018::P000::RAG Evaluation::fac04aa39b28::C000::fac04aa39b28`

**Child relevance:** `[   ]`

Document ID: DOC-018

#### Parent 1

**parent_key:** `DOC-018::P001::RAG Evaluation/Metrics::c46eea5d9f13`

**section_path:** RAG Evaluation > Metrics

**Parent relevance:** `[   ]`

Hit Rate checks whether a relevant item appears in top K. Recall@K measures coverage of known relevant items. Mean Reciprocal Rank rewards placing the first relevant item near the top.

##### Child 0

**child_key:** `DOC-018::P001::RAG Evaluation/Metrics::c46eea5d9f13::C000::d28a36e53577`

**Child relevance:** `[   ]`

Hit Rate checks whether a relevant item appears in top K. Recall@K measures coverage of known relevant items. Mean

##### Child 1

**child_key:** `DOC-018::P001::RAG Evaluation/Metrics::c46eea5d9f13::C001::8d9281b35d56`

**Child relevance:** `[   ]`

of known relevant items. Mean Reciprocal Rank rewards placing the first relevant item near the top.

#### Parent 2

**parent_key:** `DOC-018::P002::RAG Evaluation/Parents::38fe5954a8bf`

**section_path:** RAG Evaluation > Parents

**Parent relevance:** `[   ]`

Child recall and parent recall differ because several child hits may collapse to one parent. Candidate parent recall before reranking is especially important.

##### Child 0

**child_key:** `DOC-018::P002::RAG Evaluation/Parents::38fe5954a8bf::C000::19cfc0526d27`

**Child relevance:** `[   ]`

Child recall and parent recall differ because several child hits may collapse to one parent. Candidate parent recall

##### Child 1

**child_key:** `DOC-018::P002::RAG Evaluation/Parents::38fe5954a8bf::C001::99550e8ff68c`

**Child relevance:** `[   ]`

Candidate parent recall before reranking is especially important.

#### Parent 3

**parent_key:** `DOC-018::P003::RAG Evaluation/Answer::1b0b32e5b5b6`

**section_path:** RAG Evaluation > Answer

**Parent relevance:** `[   ]`

Retrieval metrics do not fully determine answer quality. Faithfulness, answer relevance, context precision, and citation correctness are separate concerns.

##### Child 0

**child_key:** `DOC-018::P003::RAG Evaluation/Answer::1b0b32e5b5b6::C000::7f1f3d5022cf`

**Child relevance:** `[   ]`

Retrieval metrics do not fully determine answer quality. Faithfulness, answer relevance, context precision, and

##### Child 1

**child_key:** `DOC-018::P003::RAG Evaluation/Answer::1b0b32e5b5b6::C001::ab7cb10bace2`

**Child relevance:** `[   ]`

context precision, and citation correctness are separate concerns.

#### Parent 4

**parent_key:** `DOC-018::P004::RAG Evaluation/Gold::b653a61ef392`

**section_path:** RAG Evaluation > Gold

**Parent relevance:** `[   ]`

A golden benchmark should include exact identifiers, semantic paraphrases, ambiguous questions, multi-section needs, and unanswerable queries.

##### Child 0

**child_key:** `DOC-018::P004::RAG Evaluation/Gold::b653a61ef392::C000::fe46b40ac0c9`

**Child relevance:** `[   ]`

A golden benchmark should include exact identifiers, semantic paraphrases, ambiguous questions, multi-section needs,

##### Child 1

**child_key:** `DOC-018::P004::RAG Evaluation/Gold::b653a61ef392::C001::581d360a5038`

**Child relevance:** `[   ]`

multi-section needs, and unanswerable queries.

### Document DOC-024

**Document relevance:** `[   ]`

#### Parent 0

**parent_key:** `DOC-024::P000::Retriever Benchmark Design::731b6a7a8646`

**section_path:** Retriever Benchmark Design

**Parent relevance:** `[   ]`

Document ID: DOC-024

##### Child 0

**child_key:** `DOC-024::P000::Retriever Benchmark Design::731b6a7a8646::C000::731b6a7a8646`

**Child relevance:** `[   ]`

Document ID: DOC-024

#### Parent 1

**parent_key:** `DOC-024::P001::Retriever Benchmark Design/Corpus::9b5ff54a3f6e`

**section_path:** Retriever Benchmark Design > Corpus

**Parent relevance:** `[   ]`

A useful benchmark is large enough that top_k cannot expose almost the whole collection. It should include overlapping topics, near-duplicates, exact identifiers, paraphrases, and plausible distractors.

##### Child 0

**child_key:** `DOC-024::P001::Retriever Benchmark Design/Corpus::9b5ff54a3f6e::C000::224db238b205`

**Child relevance:** `[   ]`

A useful benchmark is large enough that top_k cannot expose almost the whole collection. It should include overlapping

##### Child 1

**child_key:** `DOC-024::P001::Retriever Benchmark Design/Corpus::9b5ff54a3f6e::C001::a59665b15ad5`

**Child relevance:** `[   ]`

It should include overlapping topics, near-duplicates, exact identifiers, paraphrases, and plausible distractors.

#### Parent 2

**parent_key:** `DOC-024::P002::Retriever Benchmark Design/Queries::37ef4fdae550`

**section_path:** Retriever Benchmark Design > Queries

**Parent relevance:** `[   ]`

Include lexical queries like ef_construct and HTTP 422, semantic paraphrases, composite questions, and unanswerable requests.

##### Child 0

**child_key:** `DOC-024::P002::Retriever Benchmark Design/Queries::37ef4fdae550::C000::105561e18934`

**Child relevance:** `[   ]`

Include lexical queries like ef_construct and HTTP 422, semantic paraphrases, composite questions, and unanswerable

##### Child 1

**child_key:** `DOC-024::P002::Retriever Benchmark Design/Queries::37ef4fdae550::C001::105523b826bf`

**Child relevance:** `[   ]`

questions, and unanswerable requests.

#### Parent 3

**parent_key:** `DOC-024::P003::Retriever Benchmark Design/Compare::b22f3ddac893`

**section_path:** Retriever Benchmark Design > Compare

**Parent relevance:** `[   ]`

Run Dense, Sparse, Hybrid, Hybrid plus CrossEncoder, and Hybrid plus CrossEncoder plus Parent MMR against the same corpus and labels.

##### Child 0

**child_key:** `DOC-024::P003::Retriever Benchmark Design/Compare::b22f3ddac893::C000::7de797dccca4`

**Child relevance:** `[   ]`

Run Dense, Sparse, Hybrid, Hybrid plus CrossEncoder, and Hybrid plus CrossEncoder plus Parent MMR against the same

##### Child 1

**child_key:** `DOC-024::P003::Retriever Benchmark Design/Compare::b22f3ddac893::C001::ab127b704beb`

**Child relevance:** `[   ]`

Parent MMR against the same corpus and labels.

#### Parent 4

**parent_key:** `DOC-024::P004::Retriever Benchmark Design/Report::6d93b50448f8`

**section_path:** Retriever Benchmark Design > Report

**Parent relevance:** `[   ]`

Report Recall@5, Recall@10, MRR, candidate parent recall, final context precision, and latency.

##### Child 0

**child_key:** `DOC-024::P004::Retriever Benchmark Design/Report::6d93b50448f8::C000::6d93b50448f8`

**Child relevance:** `[   ]`

Report Recall@5, Recall@10, MRR, candidate parent recall, final context precision, and latency.

---

## Q032

**Query:** How do I choose the best GPU for video rendering?

**Query class:** unanswerable

**Answerability:** unanswerable

No relevant documents in the legacy benchmark.
