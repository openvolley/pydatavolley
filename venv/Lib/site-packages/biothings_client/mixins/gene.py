class MyGeneClientMixin:
    def findgenes(self, id_li, **kwargs):
        """.. deprecated:: 2.0.0
        Use :py:meth:`querymany` instead. It's kept here as an alias of :py:meth:`querymany` method.
        """
        import warnings

        warnings.warn(
            'Deprecated! Currently an alias of "querymany" method. Use "querymany" method directly.', DeprecationWarning
        )
        return self.querymany(id_li, **kwargs)
