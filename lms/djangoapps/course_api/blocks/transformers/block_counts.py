from openedx.core.lib.block_cache.transformer import BlockStructureTransformer


class BlockCountsTransformer(BlockStructureTransformer):
    """
    ...
    """
    VERSION = 1

    def __init__(self, block_types_to_count):
        self.block_types_to_count = block_types_to_count

    @classmethod
    def collect(cls, block_structure):
        """
        Collects any information that's necessary to execute this transformer's
        transform method.
        """
        # collect basic xblock fields
        block_structure.request_xblock_fields('type')

    def transform(self, user_info, block_structure):
        """
        Mutates block_structure based on the given user_info.
        """
        for block_key in block_structure.post_order_traversal():
            for block_type in self.block_types_to_count:
                descendants_type_count = sum([
                    block_structure.get_transformer_block_data(child_key, self, block_type, 0)
                    for child_key in block_structure.get_children(block_key)
                ])
                block_structure.set_transformer_block_data(
                    block_key,
                    self,
                    block_type,
                    (
                        descendants_type_count +
                        (1 if block_structure.get_xblock_field(block_key, 'type') else 0)
                    )
                )
