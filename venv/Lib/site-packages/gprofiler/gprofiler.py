from typing import Union, List, Dict, Any

import requests

from gprofiler.version import __version__


class GProfiler():
    def __init__(self, user_agent: str = '', base_url: str = None, return_dataframe: bool = False):
        '''
        A class representing the g:Profiler toolkit. Contains methods for
        querying the g:GOSt, g:Convert, g:Orth and g:SNPense tools. Please see the
        g:Profiler web tool (https://biit.cs.ut.ee/gprofiler/) for extensive documentation on all the options to
        the methods.

        :param user_agent: the URL used for the g:Profiler service.
        :param base_url: the URL used for the g:Profiler service.
        :param return_dataframe: if True, query results are presented as pandas DataFrames.
        '''
        self.user_agent = 'gprofiler-python {version}/{user_agent}'.format(version=__version__, user_agent=user_agent)

        if base_url is None:
            self.base_url = 'https://biit.cs.ut.ee/gprofiler'
        else:
            self.base_url = base_url

        self.return_dataframe = return_dataframe
        if return_dataframe:
            self._pandas = self._get_pandas_module()

        self.meta = None

    @staticmethod
    def _get_pandas_module():
        is_pandas_module = lambda x: getattr(x, '__name__', '') == 'pandas'
        namespace = globals()
        if 'pd' in namespace and is_pandas_module(namespace['pd']):
            return namespace['pd']
        elif 'pandas' in namespace and is_pandas_module(namespace['pandas']):
            return namespace['pandas']
        else:
            import importlib
            return importlib.import_module('pandas')


    def __getattr__(self, item):
        if item in ['gprofile', 'gorth', 'gconvert']:
            raise NotImplementedError('''`{}` has been renamed `{}` and has a new interface
To use the previous version use the command `pip install --upgrade --no-deps --force-reinstall gprofiler-official==0.3.5`
                    '''.format(item, item[1:]))
        raise AttributeError('{} is not an attribute of {}'.format(item, self.__class__.__name__))



    def profile(
            self,
            query: Union[str, List[str], Dict[str, List[str]]],
            organism: str = 'hsapiens',
            sources: List[str] = tuple(),
            user_threshold: float = 0.05,
            all_results: bool = False,
            ordered: bool = False,
            no_evidences: bool = True,
            combined: bool = False,
            measure_underrepresentation: bool = False,
            no_iea: bool = False,
            domain_scope: str = 'annotated',
            numeric_namespace: str = '',
            significance_threshold_method: str = 'g_SCS',
            background: str = None,

    ) -> List[Dict[str, Any]]:
        """
        performs functional profiling of gene lists using various kinds of biological evidence.
        The tool performs statistical enrichment analysis to find over-representation of information from Gene Ontology terms,
        biological pathways, regulatory DNA elements, human disease gene annotations, and protein-protein interaction networks.



        :param query: list of genes to profile. For running multiple queries at once, accepts a dictionary of lists as well.
        :param organism: Organism id for profiling. For full list see https://biit.cs.ut.ee/gprofiler/page/organism-list
        :param sources: List of annotation sources to include in analysis. Defaults to all known.
        :param user_threshold: Significance threshold for analysis.
        :param all_results: If True, return all analysis results regardless of statistical significance.
        :param ordered: If True, considers the order of input query to be significant. See https://biit.cs.ut.ee/gprofiler/page/docs#ordered_gene_lists
        :param no_evidences: If False, the results include lists of intersections and evidences for the intersections
        :param combined: If True, performs all queries and combines the results into a single table. NB! changes the output format.
        :param measure_underrepresentation: if True, performs test for significantly under-represented functional terms.
        :param no_iea: If True, excludes electronically annotated Gene Ontology terms before analysis.
        :param domain_scope: "known" for using all known genes as background, "annotated" to use all genes annotated for particular datasource.
        :param numeric_namespace: name for the numeric namespace to use if there are numeric values in the query.
        :param significance_threshold_method: method for multiple correction. "g_SCS"|"bonferroni"|"fdr". https://biit.cs.ut.ee/gprofiler/page/docs#significance_threhshold
        :param background: List of genes to use as a statistical background.
        :return:
        """

        if background is not None:
            domain_scope = 'custom'

        r = requests.post(
            '{}/api/gost/profile/'.format(self.base_url.rstrip("/")),
            json={
                'organism': organism,  # string, eg "hsapiens"
                'query': query,  # whitespace-delimited string or list of strings or object of strings to lists of strings
                'sources': sources,  # list of strings, for example:
                'user_threshold': user_threshold,  # significance threshold, defaults to 0.05
                'all_results': all_results,  # bool
                'no_evidences': no_evidences,  # bool - if set to true, saves on database lookups
                'combined': combined,  # bool, set to true for g:Cocoa output
                'measure_underrepresentation': measure_underrepresentation,  # bool
                'no_iea': no_iea,  # bool
                'numeric_ns': numeric_namespace,  # string
                'domain_scope': domain_scope,  # string 'known'|'annotated'|'custom'
                'ordered': ordered,  # bool, set to true for ordered query
                'significance_threshold_method': significance_threshold_method,  # string, "g_SCS"|"bonferroni"|"fdr", "g_SCS"by default
                'background': background if background is not None else ''  # string,  background name or query string

            }
            , headers={'User-Agent': self.user_agent})

        if r.status_code != 200:
            message = ''
            try:
                message = r.json()['message']
            except:
                message = 'query failed with error {}'.format(r.status_code)
            raise AssertionError(message)
        res = r.json()

        meta = res['meta']
        self.meta = meta

        if not combined:
            columns = ['source',
                       'native',
                       'name',
                       'p_value',
                       'significant',
                       'description',
                       'term_size',
                       'query_size',
                       'intersection_size',
                       'effective_domain_size',
                       'precision',
                       'recall',
                       'query',
                       'parents']
            if not no_evidences:
                columns.append('intersections')
                columns.append('evidences')
        else:
            columns = [
                'source',
                'native',
                'name',
                'p_values',
                'description',
                'term_size',
                'query_sizes',
                'intersection_sizes',
                'effective_domain_size',
                'parents']

        queries = (meta['query_metadata']['queries'].keys())

        if not no_evidences and not combined:
            reverse_mappings = {}
            for query in queries:
                mapping = (meta['genes_metadata']['query'][query]['mapping'])
                reverse_mapping = {}
                for k, v in mapping.items():
                    if len(v) == 1:
                        # one-to-one mapping
                        reverse_mapping[v[0]] = k
                    else:
                        # one-to=many mapping, we'll use the gene ID
                        for i in v:
                            reverse_mapping[i] = i
                reverse_mappings[query] = reverse_mapping

            for result in res['result']:
                mapping = reverse_mappings[result['query']]
                genes = []
                for i in meta['genes_metadata']['query'][result['query']]['ensgs']:
                    genes.append(mapping[i])
                result['evidences'] = [i for i in result['intersections'] if i]
                result['intersections'] = ([gene for ev, gene in zip(result['intersections'], genes) if ev])

        if not self.return_dataframe:
            columns = set(columns)

            # filter the columns
            result = [{k: v for k, v in i.items() if k in columns} for i in res['result']]
            return result

        else:

            df = self._pandas.DataFrame(res['result'])

            if len(df) > 0:
                df = df[columns]

            else:
                return self._pandas.DataFrame(columns=columns)
            return df

    def convert(
            self,
            query: Union[str, List[str], Dict[str, List[str]]],
            organism: str = 'hsapiens',
            target_namespace: str = 'ENSG',
            numeric_namespace: str = 'ENTREZGENE'
    ) -> List[Dict[str, Any]]:
        """
        Query g:Convert.

        :param query: list of genes to convert
        :param organism: organism id
        :param target_namespace: namespace to convert into
        :param numeric_namespace
        """
        r = requests.post(
            '{}/api/convert/convert'.format(self.base_url),
            json={
                'organism': organism,
                'query': query,
                'target': target_namespace,
                'numeric_ns': numeric_namespace,
                'output': 'json'
            },
            headers={'User-Agent': self.user_agent}
        )

        if r.status_code != 200:
            message = ''
            try:
                message = r.json()['message']
            except:
                message = 'query failed with error {}'.format(r.status_code)
            raise AssertionError(message)
        res = r.json()

        meta = res['meta']
        self.meta = meta
        columns = ['incoming', 'converted', 'n_incoming', 'n_converted', 'name', 'description', 'namespaces', 'query']

        if not self.return_dataframe:
            columns = set(columns)

            # filter the columns
            result = [{k: v for k, v in i.items() if k in columns} for i in res['result']]
            return result

        df = self._pandas.DataFrame(res['result'])
        df = df[columns]

        return df

    def orth(self,
             query: List[str],
             organism: str = "hsapiens",
             target: str = "mmusculus",
             aresolve: Dict[str, str] = None,
             numeric_namespace: str = 'ENTREZGENE'):
        """
        Query g:Orth.


        :param query:
        :param organism:
        :param target:
        :param aresolve:
        :param numeric_namespace:
        """
        r = requests.post(
            '{}/api/orth/orth'.format(self.base_url),
            json={
                'organism': organism,
                'query': query,
                'target': target,
                'numeric_ns': numeric_namespace,
                'aresolve': aresolve,
                'output': 'json'
            },
            headers={'User-Agent': self.user_agent}
        )

        if r.status_code != 200:
            message = ''
            try:
                message = r.json()['message']
            except:
                message = 'query failed with error {}'.format(r.status_code)
            raise AssertionError(message)
        res = r.json()
        meta = res['meta']
        self.meta = meta
        columns = ['incoming', 'converted', 'ortholog_ensg', 'n_incoming', 'n_converted', 'n_result', 'name', 'description', 'namespaces']
        if not self.return_dataframe:
            columns = set(columns)

            # filter the columns
            result = [{k: v for k, v in i.items() if k in columns} for i in res['result']]
            return result


        df = self._pandas.DataFrame(res['result'])
        df = df[columns]

        return df

    def snpense(self,
                query: List[str]):
        """

        :param query:
        """
        r = requests.post(
            '{}/api/snpense/snpense'.format(self.base_url),
            json={
                'query': query,
                'output': 'json+'
            },
            headers={'User-Agent': self.user_agent}
        )

        if r.status_code != 200:
            message = ''
            try:
                message = r.json()['message']
            except:
                message = 'query failed with error {}'.format(r.status_code)
            raise AssertionError(message)
        res = r.json()
        meta = res['meta']
        self.meta = meta
        columns = ['rs_id', 'chromosome', 'strand', 'start', 'end', 'ensgs', 'gene_names', 'variants']
        if not self.return_dataframe:
            columns = set(columns)

            # filter the columns
            result = [{k: v for k, v in i.items() if k in columns} for i in res['result']]
            return result

        df = self._pandas.DataFrame(res['result'])
        df = df[columns]

        return df
