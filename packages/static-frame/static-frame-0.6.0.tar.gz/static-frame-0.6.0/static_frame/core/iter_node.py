'''
Tools for iterators in Series and Frame. These components are imported by both series.py and frame.py; these components also need to be able to return Series and Frame, and thus use deferred, function-based imports.
'''

import typing as tp
from enum import Enum
from functools import partial

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor

import numpy as np

# from static_frame.core.util import CallableOrMapping
from static_frame.core.util import AnyCallable
from static_frame.core.util import DtypeSpecifier
from static_frame.core.util import Mapping
from static_frame.core.doc_str import doc_inject

if tp.TYPE_CHECKING:
    from static_frame.core.frame import Frame # pylint: disable=W0611 #pragma: no cover
    from static_frame.core.series import Series # pylint: disable=W0611 #pragma: no cover


FrameOrSeries = tp.TypeVar('FrameOrSeries', 'Frame', 'Series')


class IterNodeApplyType(Enum):
    SERIES_ITEMS = 1
    SERIES_ITEMS_FLAT = 2 # do not use index class on container
    FRAME_ELEMENTS = 3
    INDEX_LABELS = 4


class IterNodeType(Enum):
    VALUES = 1
    ITEMS = 2


class IterNodeDelegate(tp.Generic[FrameOrSeries]):
    '''
    Delegate returned from :py:class:`static_frame.IterNode`, providing iteration as well as a family of apply methods.
    '''

    __slots__ = (
            '_func_values',
            '_func_items',
            '_yield_type',
            '_apply_constructor'
            )

    def __init__(self,
            func_values: tp.Callable[..., tp.Iterable[tp.Any]],
            func_items: tp.Callable[..., tp.Iterable[tp.Tuple[tp.Any, tp.Any]]],
            yield_type: IterNodeType,
            apply_constructor: tp.Callable[..., FrameOrSeries]
        ) -> None:
        '''
        Args:
            apply_constructor: Callable (generally a class) used to construct the object returned from apply(); must take an iterator of items.
        '''
        self._func_values = func_values
        self._func_items = func_items
        self._yield_type = yield_type
        self._apply_constructor: tp.Callable[..., FrameOrSeries] = apply_constructor

    #---------------------------------------------------------------------------

    def _apply_iter_items_parallel(self,
            func: AnyCallable,
            max_workers: tp.Optional[int] = None,
            chunksize: int = 1,
            use_threads: bool = False,
            ) -> tp.Generator[tp.Tuple[tp.Any, tp.Any], None, None]:

        pool_executor = ThreadPoolExecutor if use_threads else ProcessPoolExecutor

        yt_is_values = self._yield_type is IterNodeType.VALUES

        if not callable(func):
            func = getattr(func, '__getitem__')

        # use side effect list population to create keys when iterating over values
        func_keys = []

        arg_gen: tp.Callable[[], tp.Union[tp.Iterator[tp.Any], tp.Iterator[tp.Tuple[tp.Any, tp.Any]]]]

        if yt_is_values:
            def arg_gen() -> tp.Iterator[tp.Any]: #pylint: disable=E0102
                for k, v in self._func_items():
                    func_keys.append(k)
                    yield v
        else:
            def arg_gen() -> tp.Iterator[tp.Tuple[tp.Any, tp.Any]]: #pylint: disable=E0102
                for k, v in self._func_items():
                    func_keys.append(k)
                    yield k, v

        with pool_executor(max_workers=max_workers) as executor:
            yield from zip(func_keys,
                    executor.map(func, arg_gen(), chunksize=chunksize)
                    )

    #---------------------------------------------------------------------------
    # public interface

    @doc_inject(selector='map_any')
    def map_any_iter_items(self,
            mapping: Mapping
            ) -> tp.Iterator[tp.Tuple[tp.Any, tp.Any]]:
        '''
        {doc} A generator of resulting key, value pairs.

        Args:
            {mapping}
        '''
        get = getattr(mapping, 'get')
        func: AnyCallable = lambda k: get(k, k)
        if self._yield_type is IterNodeType.VALUES:
            yield from ((k, func(v)) for k, v in self._func_items())
        else:
            yield from ((k, func(k,  v)) for k, v in self._func_items())

    @doc_inject(selector='map_any')
    def map_any_iter(self,
            mapping: Mapping,
            ) -> tp.Iterator[tp.Any]:
        '''
        {doc} A generator of resulting values.

        Args:
            {mapping}
        '''
        yield from (v for _, v in self.map_any_iter_items(mapping))

    @doc_inject(selector='map_any')
    def map_any(self,
            mapping: Mapping,
            *,
            dtype: DtypeSpecifier = None
            ) -> FrameOrSeries:
        '''
        {doc} Returns a new container.

        Args:
            {mapping}
            {dtype}
        '''
        return self._apply_constructor(
                self.map_any_iter_items(mapping),
                dtype=dtype)


    #---------------------------------------------------------------------------
    @doc_inject(selector='map_fill')
    def map_fill_iter_items(self,
            mapping: Mapping,
            *,
            fill_value: tp.Any = np.nan,
            ) -> tp.Iterator[tp.Tuple[tp.Any, tp.Any]]:
        '''
        {doc} A generator of resulting key, value pairs.

        Args:
            {mapping}
            {fill_value}
        '''
        get = getattr(mapping, 'get')
        func: AnyCallable = lambda k: get(k, fill_value)
        if self._yield_type is IterNodeType.VALUES:
            yield from ((k, func(v)) for k, v in self._func_items())
        else:
            yield from ((k, func(k,  v)) for k, v in self._func_items())

    @doc_inject(selector='map_fill')
    def map_fill_iter(self,
            mapping: Mapping,
            *,
            fill_value: tp.Any = np.nan,
            ) -> tp.Iterator[tp.Any]:
        '''
        {doc} A generator of resulting values.

        Args:
            {mapping}
            {fill_value}
        '''
        yield from (v for _, v in self.map_fill_iter_items(mapping, fill_value=fill_value))

    @doc_inject(selector='map_fill')
    def map_fill(self,
            mapping: Mapping,
            *,
            fill_value: tp.Any = np.nan,
            dtype: DtypeSpecifier = None
            ) -> FrameOrSeries:
        '''
        {doc} Returns a new container.

        Args:
            {mapping}
            {fill_value}
            {dtype}
        '''
        return self._apply_constructor(
                self.map_fill_iter_items(mapping, fill_value=fill_value),
                dtype=dtype)

    #---------------------------------------------------------------------------
    @doc_inject(selector='map_all')
    def map_all_iter_items(self,
            mapping: Mapping
            ) -> tp.Iterator[tp.Tuple[tp.Any, tp.Any]]:
        '''
        {doc} A generator of resulting key, value pairs.

        Args:
            {mapping}
        '''
        func = getattr(mapping, '__getitem__')
        if self._yield_type is IterNodeType.VALUES:
            yield from ((k, func(v)) for k, v in self._func_items())
        else:
            yield from ((k, func(k,  v)) for k, v in self._func_items())

    @doc_inject(selector='map_all')
    def map_all_iter(self,
            mapping: Mapping
            ) -> tp.Iterator[tp.Any]:
        '''
        {doc} A generator of resulting values.

        Args:
            {mapping}
        '''
        yield from (v for _, v in self.map_all_iter_items(mapping=mapping))

    @doc_inject(selector='map_all')
    def map_all(self,
            mapping: Mapping,
            *,
            dtype: DtypeSpecifier = None
            ) -> FrameOrSeries:
        '''
        {doc} Returns a new container.

        Args:
            {mapping}
            {dtype}
        '''
        return self._apply_constructor(
                self.map_all_iter_items(mapping),
                dtype=dtype)


    #---------------------------------------------------------------------------
    @doc_inject(selector='apply')
    def apply_iter_items(self,
            func: AnyCallable) -> tp.Iterator[tp.Tuple[tp.Any, tp.Any]]:
        '''
        {doc} A generator of resulting key, value pairs.

        Args:
            {func}
        '''
        # depend on yield type, we determine what the passed in function expects to take
        if self._yield_type is IterNodeType.VALUES:
            yield from ((k, func(v)) for k, v in self._func_items())
        else:
            yield from ((k, func(k, v)) for k, v in self._func_items())

    @doc_inject(selector='apply')
    def apply_iter(self,
            func: AnyCallable
            ) -> tp.Iterator[tp.Any]:
        '''
        {doc} A generator of resulting values.

        Args:
            {func}
        '''
        yield from (v for _, v in self.apply_iter_items(func=func))

    @doc_inject(selector='apply')
    def apply(self,
            func: AnyCallable,
            *,
            dtype: DtypeSpecifier = None
            ) -> FrameOrSeries:
        '''
        {doc} Returns a new container.

        Args:
            {func}
            {dtype}
        '''
        if not callable(func):
            raise RuntimeError('use map_fill(), map_any(), or map_all() for applying a mapping type')

        return self._apply_constructor(
                self.apply_iter_items(func),
                dtype=dtype)


    def apply_pool(self,
            func: AnyCallable,
            *,
            dtype: DtypeSpecifier = None,
            max_workers: tp.Optional[int] = None,
            chunksize: int = 1,
            use_threads: bool = False
            ) -> FrameOrSeries:
        '''
        Apply passed function to each object iterated, where the object depends on the creation of this instance. Employ parallel processing with either the ProcessPoolExecutor or ThreadPoolExecutor.

        Args:
            func: A function.
            dtype: Type used to create the returned array.
            max_workers: Passed to the pool_executor, where None defaults to the max number of machine processes.
            chunksize: Passed to the pool executor.
            use_thread: When True, the ThreadPoolExecutor will be used rather than the default ProcessPoolExecutor.
        '''
        return self._apply_constructor(
                self._apply_iter_items_parallel(
                        func=func,
                        max_workers=max_workers,
                        chunksize=chunksize,
                        use_threads=use_threads),
                dtype=dtype)

    def __iter__(self) -> tp.Union[tp.Iterator[tp.Any], tp.Iterator[tp.Tuple[tp.Any, tp.Any]]]:
        '''
        Return a generator based on the yield type.
        '''
        if self._yield_type is IterNodeType.VALUES:
            yield from self._func_values()
        else:
            yield from self._func_items()



#-------------------------------------------------------------------------------

class IterNode(tp.Generic[FrameOrSeries]):
    '''Interface to a type of iteration on :py:class:`static_frame.Series` and :py:class:`static_frame.Frame`.
    '''
    # '''Stores two version of a generator function: one to yield single values, another to yield items pairs. The latter is needed in all cases, as when we use apply we return a Series, and need to have recourse to an index.
    # '''

    __slots__ = (
            '_container',
            '_func_values',
            '_func_items',
            '_yield_type',
            '_apply_type'
            )

    def __init__(self, *,
            container: FrameOrSeries,
            function_values: tp.Callable[..., tp.Iterable[tp.Any]],
            function_items: tp.Callable[..., tp.Iterable[tp.Tuple[tp.Any, tp.Any]]],
            yield_type: IterNodeType,
            apply_type: IterNodeApplyType = IterNodeApplyType.SERIES_ITEMS
            ) -> None:

        self._container: FrameOrSeries = container
        self._func_values = function_values
        self._func_items = function_items
        self._yield_type = yield_type
        self._apply_type = apply_type

    # Returns IterNodeDelegate... may need some TypeVar wizardry here...
    def __call__(self, *args: object, **kwargs: object) -> IterNodeDelegate[FrameOrSeries]:
        '''
        In usage as an iteator, the args passed here are expected to be argument for the core iterators, i.e., axis arguments.
        '''
        from static_frame.core.series import Series
        from static_frame.core.frame import Frame
        from static_frame.core.frame import Index

        func_values = partial(self._func_values, *args, **kwargs)
        func_items = partial(self._func_items, *args, **kwargs)

        apply_constructor: tp.Callable[..., tp.Union[Frame, Series]]

        if self._apply_type is IterNodeApplyType.SERIES_ITEMS:
            # always return a Series
            apply_constructor = partial(
                    Series.from_items,
                    index_constructor=self._container.index.from_labels
                    )
        elif self._apply_type is IterNodeApplyType.SERIES_ITEMS_FLAT:
            # use default index constructor
            apply_constructor = Series.from_items

        elif self._apply_type is IterNodeApplyType.FRAME_ELEMENTS:
            assert isinstance(self._container, Frame) # for typing
            apply_constructor = partial(
                    self._container.__class__.from_element_loc_items,
                    index=self._container._index,
                    columns=self._container._columns,
                    index_constructor=self._container._index.from_labels,
                    columns_constructor=self._container._columns.from_labels
                    )
        elif self._apply_type is IterNodeApplyType.INDEX_LABELS:
            # when this is used with hierarchical indices, we are likely to not get a unique values; thus, passing this to an Index constructor is awkward. instead, simply create a Series
            # import ipdb; ipdb.set_trace()
            apply_constructor = Series.from_items
        else:
            raise NotImplementedError()

        return IterNodeDelegate(
                func_values=func_values,
                func_items=func_items,
                yield_type=self._yield_type,
                apply_constructor=tp.cast(tp.Callable[..., FrameOrSeries], apply_constructor)
                )
