# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
# Copyright 2024 and onwards Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pynini
from pynini.lib import pynutil

from nemo_text_processing.inverse_text_normalization.hi.graph_utils import GraphFst, delete_extra_space, delete_space
from nemo_text_processing.inverse_text_normalization.hi.verbalizers.verbalize import VerbalizeFst
from nemo_text_processing.inverse_text_normalization.hi.verbalizers.word import WordFst


class VerbalizeFinalFst(GraphFst):
    """
    Finite state transducer that verbalizes an entire sentence, e.g.
    tokens { name: "अब" } tokens { time { hours: "१२" minutes: "३०" } } tokens { name: "बज" } tokens { name: "गए" } tokens { name: "हैं" } -> अब १२:३० बज गए हैं
    """

    def __init__(self):
        super().__init__(name="verbalize_final", kind="verbalize")
        verbalize = VerbalizeFst().fst
        word = WordFst().fst
        types = verbalize | word
        graph = (
            pynutil.delete("tokens")
            + delete_space
            + pynutil.delete("{")
            + delete_space
            + types
            + delete_space
            + pynutil.delete("}")
        )
        graph = delete_space + pynini.closure(graph + delete_extra_space) + graph + delete_space
        self.fst = graph
