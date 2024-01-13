DOCSTRING = {
    "getvariant": """Return the variant object for the give HGVS-based variant id.
        This is a wrapper for GET query of "/variant/<hgvsid>" service.

        :param vid: an HGVS-based variant id. `More about HGVS id <http://docs.myvariant.info/en/latest/doc/data.html#id-field>`_.
        :param fields: fields to return, a list or a comma-separated string.
                       If not provided or **fields="all"**, all available fields
                       are returned. See `here <http://docs.myvariant.info/en/latest/doc/data.html#available-fields>`_
                       for all available fields.
        :param assembly: specify the human genome assembly used in HGVS-based variant id, "hg19" (default) or "hg38".

        :return: a variant object as a dictionary, or None if vid is not found.

        Example:

        >>> mv.getvariant('chr9:g.107620835G>A')
        >>> mv.getvariant('chr9:g.107620835G>A', fields='dbnsfp.genename')
        >>> mv.getvariant('chr9:g.107620835G>A', fields=['dbnsfp.genename', 'cadd.phred'])
        >>> mv.getvariant('chr9:g.107620835G>A', fields='all')
        >>> mv.getvariant('chr1:g.161362951G>A', assembly='hg38')

        .. Hint:: The supported field names passed to **fields** parameter can be found from
                  any full variant object (without **fields**, or **fields="all"**). Note that field name supports dot
                  notation for nested data structure as well, e.g. you can pass "dbnsfp.genename" or
                  "cadd.phred".
        """,
    "getvariants": """Return the list of variant annotation objects for the given list of hgvs-base varaint ids.
        This is a wrapper for POST query of "/variant" service.

        :param ids: a list/tuple/iterable or a string of comma-separated HGVS ids.
                    `More about hgvs id <http://docs.myvariant.info/en/latest/doc/data.html#id-field>`_.
        :param fields: fields to return, a list or a comma-separated string.
                       If not provided or **fields="all"**, all available fields
                       are returned. See `here <http://docs.myvariant.info/en/latest/doc/data.html#available-fields>`_
                       for all available fields.
        :param assembly: specify the human genome assembly used in HGVS-based variant id, "hg19" (default) or "hg38".
        :param as_generator:  if True, will yield the results in a generator.
        :param as_dataframe: if True or 1 or 2, return object as DataFrame (requires Pandas).
                                  True or 1: using json_normalize
                                  2        : using DataFrame.from_dict
                                  otherwise: return original json
        :param df_index: if True (default), index returned DataFrame by 'query',
                         otherwise, index by number. Only applicable if as_dataframe=True.

        :return: a list of variant objects or a pandas DataFrame object (when **as_dataframe** is True)

        :ref: http://docs.myvariant.info/en/latest/doc/variant_annotation_service.html.

        Example:

        >>> vars = ['chr1:g.866422C>T',
        ...         'chr1:g.876664G>A',
        ...         'chr1:g.69635G>C',
        ...         'chr1:g.69869T>A',
        ...         'chr1:g.881918G>A',
        ...         'chr1:g.865625G>A',
        ...         'chr1:g.69892T>C',
        ...         'chr1:g.879381C>T',
        ...         'chr1:g.878330C>G']
        >>> mv.getvariants(vars, fields="cadd.phred")
        >>> mv.getvariants('chr1:g.876664G>A,chr1:g.881918G>A', fields="all")
        >>> mv.getvariants(['chr1:g.876664G>A', 'chr1:g.881918G>A'], as_dataframe=True)
        >>> mv.getvariants(['chr1:g.161362951G>A', 'chr2:g.51032181G>A'], assembly='hg38')

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

        :param q: a query string, detailed query syntax `here <http://docs.myvariant.info/en/latest/doc/variant_query_service.html#query-syntax>`_.
        :param fields: fields to return, a list or a comma-separated string.
                       If not provided or **fields="all"**, all available fields
                       are returned. See `here <http://docs.myvariant.info/en/latest/doc/data.html#available-fields>`_
                       for all available fields.
        :param assembly: specify the human genome assembly used for the query, "hg19" (default) or "hg38".
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
        :ref: http://docs.myvariant.info/en/latest/doc/variant_query_service.html.

        Example:

        >>> mv.query('_exists_:dbsnp AND _exists_:cosmic')
        >>> mv.query('dbnsfp.polyphen2.hdiv.score:>0.99 AND chrom:1')
        >>> mv.query('cadd.phred:>50')
        >>> mv.query('dbnsfp.genename:CDK2', size=5)
        >>> mv.query('dbnsfp.genename:CDK2', size=5, assembly='hg38')
        >>> mv.query('dbnsfp.genename:CDK2', fetch_all=True)
        >>> mv.query('chrX:151073054-151383976')

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
        :param assembly: specify the human genome assembly used for the query, "hg19" (default) or "hg38".
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

        >>> mv.querymany(['rs58991260', 'rs2500'], scopes='dbsnp.rsid')
        >>> mv.querymany(['rs58991260', 'rs2500'], scopes='dbsnp.rsid', assembly='hg38')
        >>> mv.querymany(['RCV000083620', 'RCV000083611', 'RCV000083584'], scopes='clinvar.rcv_accession')
        >>> mv.querymany(['COSM1362966', 'COSM990046', 'COSM1392449'], scopes='cosmic.cosmic_id', fields='cosmic')
        >>> mv.querymany(['COSM1362966', 'COSM990046', 'COSM1392449'], scopes='cosmic.cosmic_id',
        ...              fields='cosmic.tumor_site', as_dataframe=True)

        .. Hint:: :py:meth:`querymany` is perfect for query variants based different ids, e.g. rsid, clinvar ids, etc.

        .. Hint:: Just like :py:meth:`getvariants`, passing a large list of ids (>1000) to :py:meth:`querymany` is perfectly fine.

        .. Hint:: If you need to pass a very large list of input qterms, you can pass a generator
                  instead of a full list, which is more memory efficient.

        """,
    "metadata": """Return a dictionary of MyVariant.info metadata.

        :param assembly: return the metadata for either hg19 or hg38 variants, "hg19" (default) or "hg38".

        Example:

        >>> metadata = mv.metadata()
        >>> metadata = mv.metadata(assembly='hg38')

        """,
    "get_fields": """Wrapper for http://myvariant.info/v1/metadata/fields

        :param search_term: a case insensitive string to search for in available field names.
                            If not provided, all available fields will be returned.

        :param assembly: return the metadata for either hg19 or hg38 variants, "hg19" (default) or "hg38".

        Example:

        >>> mv.get_fields()
        >>> mv.get_fields("rsid")
        >>> mv.get_fields("sift")

        .. Hint:: This is useful to find out the field names you need to pass to **fields** parameter of other methods.

        """,
}
