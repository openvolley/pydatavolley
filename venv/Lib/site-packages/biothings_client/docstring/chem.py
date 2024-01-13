DOCSTRING = {
    "getchem": """Return the chemical/drug object for the give id.
        This is a wrapper for GET query of "/chem/<chem_id>" service.

        :param _id: a chemical/drug id, supports InchiKey, Drugbank ID, ChEMBL ID, ChEBI ID, PubChem CID and UNII.
                    `More about chemical/drug id <http://docs.mychem.info/en/latest/doc/data.html#id-field>`_.
        :param fields: fields to return, a list or a comma-separated string.
                       If not provided or **fields="all"**, all available fields
                       are returned. See `here <http://docs.mychem.info/en/latest/doc/data.html#available-fields>`_
                       for all available fields.

        :return: a chemical/drug object as a dictionary, or None if _id is not found.

        Example:

        >>> mc.getchem("ZRALSGWEFCBTJO-UHFFFAOYSA-N")
        >>> mc.getchem("DB00553", fields="chebi.name,drugbank.id,pubchem.cid")
        >>> mc.getchem("CHEMBL1308", fields=["chebi.name", "drugbank.id", "pubchem.cid"])
        >>> mc.getchem("7AXV542LZ4", fields="unii")
        >>> mc.getchem("CHEBI:6431", fields="chembl.smiles")

        .. Hint:: The supported field names passed to **fields** parameter can be found from
                  any full chemical/drug object (without **fields**, or **fields="all"**). Note that field name supports dot
                  notation for nested data structure as well, e.g. you can pass "drugbank.id" or
                  "chembl.smiles".
        """,
    "getchems": """Return the list of chemical/drug annotation objects for the given list of chemical/drug ids.
        This is a wrapper for POST query of "/chem" service.

        :param ids: a list/tuple/iterable or a string of comma-separated chem/drug ids.
                    `More about chem/drug id <http://docs.mychem.info/en/latest/doc/data.html#id-field>`_.
        :param fields: fields to return, a list or a comma-separated string.
                       If not provided or **fields="all"**, all available fields
                       are returned. See `here <http://docs.mychem.info/en/latest/doc/data.html#available-fields>`_
                       for all available fields.
        :param as_generator:  if True, will yield the results in a generator.
        :param as_dataframe: if True or 1 or 2, return object as DataFrame (requires Pandas).
                                  True or 1: using json_normalize
                                  2        : using DataFrame.from_dict
                                  otherwise: return original json
        :param df_index: if True (default), index returned DataFrame by 'query',
                         otherwise, index by number. Only applicable if as_dataframe=True.

        :return: a list of variant objects or a pandas DataFrame object (when **as_dataframe** is True)

        :ref: http://docs.mychem.info/en/latest/doc/chem_annotation_service.html.

        Example:

        >>> chems = [
        ...     "KTUFNOKKBVMGRW-UHFFFAOYSA-N",
        ...     "HXHWSAZORRCQMX-UHFFFAOYSA-N",
        ...     "DQMZLTXERSFNPB-UHFFFAOYSA-N"
        ... ]
        >>> mc.getchems(chems, fields="pubchem")
        >>> mc.getchems('KTUFNOKKBVMGRW-UHFFFAOYSA-N,DB00553', fields="all")
        >>> mc.getchems(chems, fields='chembl', as_dataframe=True)

        .. Hint:: A large list of more than 1000 input ids will be sent to the backend
                  web service in batches (1000 at a time), and then the results will be
                  concatenated together. So, from the user-end, it's exactly the same as
                  passing a shorter list. You don't need to worry about saturating our
                  backend servers.

        .. Hint:: If you need to pass a very large list of input ids, you can pass a generator
                  instead of a full list, which is more memory efficient.
        """,
    "query": """Return  the query result.
        This is a wrapper for GET query of "/query?q=<query>" service.

        :param q: a query string, detailed query syntax `here <http://docs.mychem.info/en/latest/doc/chem_query_service.html#query-syntax>`_.
        :param fields: fields to return, a list or a comma-separated string.
                       If not provided or **fields="all"**, all available fields
                       are returned. See `here <http://docs.mychem.info/en/latest/doc/data.html#available-fields>`_
                       for all available fields.
        :param size:   the maximum number of results to return (with a cap
                       of 1000 at the moment). Default: 10.
        :param skip:   the number of results to skip. Default: 0.
        :param sort:   Prefix with "-" for descending order, otherwise in ascending order.
                       Default: sort by matching scores in decending order.
        :param as_dataframe: if True or 1 or 2, return object as DataFrame (requires Pandas).
                                  True or 1: using json_normalize
                                  2        : using DataFrame.from_dict
                                  otherwise: return original json
        :param fetch_all: if True, return a generator to all query results (unsorted).  This can provide a very fast
                          return of all hits from a large query.
                          Server requests are done in blocks of 1000 and yielded individually.  Each 1000 block of
                          results must be yielded within 1 minute, otherwise the request will expire at server side.

        :return: a dictionary with returned variant hits or a pandas DataFrame object (when **as_dataframe** is True)
                 or a generator of all hits (when **fetch_all** is True)
        :ref: http://docs.mychem.info/en/latest/doc/chem_query_service.html.

        Example:

        >>> mc.query('drugbank.name:monobenzone')
        >>> mc.query('drugbank.targets.uniprot:P07998')
        >>> mc.query('drugbank.targets.uniprot:P07998 AND _exists_:unii')
        >>> mc.query('chebi.mass:[300 TO 500]')
        >>> mc.query('sider.side_effect.name:anaemia', size=5)
        >>> mc.query('sider.side_effect.name:anaemia', fetch_all=True)

        .. Hint:: By default, **query** method returns the first 10 hits if the matched hits are >10. If the total number
                  of hits are less than 1000, you can increase the value for **size** parameter. For a query returns
                  more than 1000 hits, you can pass "fetch_all=True" to return a `generator <http://www.learnpython.org/en/Generators>`_
                  of all matching hits (internally, those hits are requested from the server-side in blocks of 1000).
        """,
    "querymany": """Return the batch query result.
        This is a wrapper for POST query of "/query" service.

        :param qterms: a list/tuple/iterable of query terms, or a string of comma-separated query terms.
        :param scopes: specify the type (or types) of identifiers passed to **qterms**, either a list or a comma-separated fields to specify type of
                       input qterms, e.g. "dbsnp.rsid", "clinvar.rcv_accession", ["dbsnp.rsid", "cosmic.cosmic_id"].
                       See `here <http://docs.myvariant.info/en/latest/doc/data.html#available-fields>`_ for full list
                       of supported fields.
        :param fields: fields to return, a list or a comma-separated string.
                       If not provided or **fields="all"**, all available fields
                       are returned. See `here <http://docs.myvariant.info/en/latest/doc/data.html#available-fields>`_
                       for all available fields.
        :param returnall:   if True, return a dict of all related data, including dup. and missing qterms
        :param verbose:     if True (default), print out information about dup and missing qterms
        :param as_dataframe: if True or 1 or 2, return object as DataFrame (requires Pandas).
                                  True or 1: using json_normalize
                                  2        : using DataFrame.from_dict
                                  otherwise: return original json
        :param df_index: if True (default), index returned DataFrame by 'query',
                         otherwise, index by number. Only applicable if as_dataframe=True.
        :return: a list of matching variant objects or a pandas DataFrame object.
        :ref: http://docs.myvariant.info/en/latest/doc/variant_query_service.html for available
              fields, extra *kwargs* and more.

        Example:

        >>> mc.querymany(["ZRALSGWEFCBTJO-UHFFFAOYSA-N", "RRUDCFGSUDOHDG-UHFFFAOYSA-N"])
        >>> mc.querymany(["DB00536", 'DB00533'], scopes='drugbank.id')
        >>> mc.querymany(["CHEBI:95222", 'CHEBI:45924', 'CHEBI:33325'], scopes='chebi.id')
        >>> mc.querymany(["CHEMBL1555813", 'CHEMBL22', 'CHEMBL842'], scopes='chembl.molecule_chembl_id')
        >>> mc.querymany(["DB00536", '4RZ82L2GY5'], scopes='drugbank.id,unii.unii')
        >>> mc.querymany(["DB00536", '4RZ82L2GY5'], scopes=['drugbank.id', 'unii.unii'])
        >>> mc.querymany(["DB00536", '4RZ82L2GY5'], scopes=['drugbank.id', 'unii.unii'], fields='drugbank,unii')
        >>> mc.querymany(["DB00536", '4RZ82L2GY5'], scopes=['drugbank.id', 'unii.unii'],
        ...              fields='drugbank.name,unii',as_dataframe=True)

        .. Hint:: :py:meth:`querymany` is perfect for query variants based different ids, e.g. rsid, clinvar ids, etc.

        .. Hint:: Just like :py:meth:`getvariants`, passing a large list of ids (>1000) to :py:meth:`querymany` is perfectly fine.

        .. Hint:: If you need to pass a very large list of input qterms, you can pass a generator
                  instead of a full list, which is more memory efficient.

        """,
    "metadata": """Return a dictionary of MyChem.info metadata, a wrapper for http://mychem.info/v1/metadata

        Example:

        >>> metadata = mv.metadata()

        """,
    "get_fields": """Wrapper for http://mychem.info/v1/metadata/fields

        :param search_term: a case insensitive string to search for in available field names.
                            If not provided, all available fields will be returned.


        Example:

        >>> mc.get_fields()
        >>> mc.get_fields("pubchem")
        >>> mc.get_fields("drugbank.targets")

        .. Hint:: This is useful to find out the field names you need to pass to **fields** parameter of other methods.

        """,
}
