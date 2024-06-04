"""
Tests custom rdflib tools

"""
import rdflib
from urllib.parse import urlsplit, urlunsplit
from rdflib import Graph, URIRef, RDF
# from rdflib.compare import graph_diff
from jinja2 import Template
from metadata_writer.logger.cmw_logger import logger
from metadata_writer.commons.query_class import QueryRetriever
from metadata_writer.commons.constants import Constants
from metadata_writer.commons.rdf_utils import are_same_graphs, get_updated_graphs_diffs
import pytest
import pytest
import os
import glob
from os import path
import rdfc10
from rdfc10.rdfc10 import Rdfc10
from rdflib import Graph
from rdflib.compare import to_isomorphic, graph_diff


@pytest.fixture
def graph_3():
    graph_3 = """
        @prefix ebucore: <http://www.ebu.ch/metadata/ontologies/ebucore/ebucore#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        [] a ebucore:Episode ;
            ebucore:assetType <https://metadata.amagi.tv/skos/amagi_ebu_AssetTypeCS#_1.2.1> ;
            ebucore:hasRelatedMediaResource [ a ebucore:MediaResource ;
                ebucore:duration "7610" ;
                ebucore:hasResourceLocator "https://formula2.mp4" ;
                ebucore:width 1920 ];
            ebucore:hasPart [ a ebucore:Part ;
                    ebucore:endOffsetNormalPlayTime "1000.067" ;
                    ebucore:hasPartType "soft" ;
                    ebucore:partId "2" ;
                    ebucore:startOffsetNormalPlayTime "533.901" ];
            ebucore:hasSubtitling [ a ebucore:ClosedSubtitling ;
                    ebucore:hasResourceLocator "RESOURCE_URL_3" ] ;
            ebucore:hasRelatedImage [ a ebucore:Thumbnail ;
                    ebucore:hasResourceLocator "RESOURCE_URL_10" ] ;
            ebucore:title "Levels of Luxury in Laos".
    """
    return rdflib.Graph().parse(data=graph_3, format='ttl')


@pytest.fixture
def graph_4():
    graph_4 = """
        @prefix ebucore: <http://www.ebu.ch/metadata/ontologies/ebucore/ebucore#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        [] a ebucore:Episode ;
            ebucore:assetType <https://metadata.amagi.tv/skos/amagi_ebu_AssetTypeCS#_1.2.1> ;
            ebucore:hasRelatedMediaResource [ a ebucore:MediaResource ;
                ebucore:duration "7610" ;
                ebucore:hasResourceLocator "https://formula1.mp4" ;
                ebucore:width 1920 ];
            ebucore:hasPart [ a ebucore:Part ;
                    ebucore:endOffsetNormalPlayTime "1000.067" ;
                    ebucore:hasPartType "soft" ;
                    ebucore:partId "2" ;
                    ebucore:startOffsetNormalPlayTime "533.901" ];
            ebucore:hasSubtitling [ a ebucore:ClosedSubtitling ;
                    ebucore:hasResourceLocator "RESOURCE_URL_4" ] ;
            ebucore:hasRelatedImage [ a ebucore:Thumbnail ;
                    ebucore:hasResourceLocator "RESOURCE_URL_11" ] ;
            ebucore:title "Levels of Luxury in Laos".
    """
    return rdflib.Graph().parse(data=graph_4, format='ttl')


def test_get_updated_graphs_diffs(graph_3, graph_4):
    # graph_1 will be the new incoming graph,
    # graph_2 will be the graph in gms;
    is_same, in_first, in_second = rdfc10.graph_diff(graph_3, graph_4)
    print(in_first.serialize(format='ttl'))
    # gives output :
    """
        @prefix ns1: <http://www.ebu.ch/metadata/ontologies/ebucore/ebucore#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
        
        [] a ns1:Episode ;
            ns1:assetType <https://metadata.amagi.tv/skos/amagi_ebu_AssetTypeCS#_1.2.1> ;
            ns1:hasPart [ ] ;
            ns1:hasRelatedImage [ ns1:hasResourceLocator "RESOURCE_URL_10" ] ;
            ns1:hasRelatedMediaResource [ a ns1:MediaResource ;
                    ns1:duration "7610" ;
                    ns1:hasResourceLocator "https://formula2.mp4" ;
                    ns1:width 1920 ] ;
            ns1:hasSubtitling [ a ns1:ClosedSubtitling ;
                    ns1:hasResourceLocator "RESOURCE_URL_3" ] ;
            ns1:title "Levels of Luxury in Laos" .
    """

    is_same, in_first, in_second = graph_diff(graph_3, graph_4)
    print(in_first.serialize(format='ttl'))

    # gives output :
    """
        @prefix ns1: <http://www.ebu.ch/metadata/ontologies/ebucore/ebucore#> .

        [] ns1:hasResourceLocator "RESOURCE_URL_3" .

        [] ns1:hasRelatedImage [ a ns1:Thumbnail ;
                    ns1:hasResourceLocator "RESOURCE_URL_10" ] .

        [] ns1:hasResourceLocator "https://formula2.mp4" .

    """
    # The second output is correct





