""" Gene specific utils. """
from collections import OrderedDict

from biothings_client import get_client


def get_homologs(gene_list, fields="all", species="all"):
    """Return the gene-objects for homologs in species for each gene in the input *gene_list*."""
    gene_client = get_client("gene")
    clean_species = [int(s) for s in species.split(",")] if species != "all" else []
    initial = OrderedDict()
    qset = set()

    for gene in gene_client.getgenes(gene_list, fields="homologene", species="all"):
        if gene["_id"] in initial:
            continue
        initial[gene["_id"]] = {}
        for taxid, geneid in gene.get("homologene", {}).get("genes", []):
            if not clean_species or taxid in clean_species:
                initial[gene["_id"]].setdefault(taxid, []).append(geneid)
                qset.add(geneid)
    gene_dict = dict([(g["_id"], g) for g in gene_client.getgenes(iter(qset), fields=fields, species="all")])

    ret = []
    for geneid, homolog_dict in initial.items():
        _ret = {"gene": geneid, "homologs": []}
        for taxid, glist in homolog_dict.items():
            _d = {"taxid": taxid, "genes": []}
            for g in glist:
                if str(g) in gene_dict:
                    _d["genes"].append(gene_dict[str(g)])
            if len(_d["genes"]) > 0:
                _ret["homologs"].append(_d)
        ret.append(_ret)

    return ret
