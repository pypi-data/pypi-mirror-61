import logging

from isc_common.http.DSRequest import DSRequest
from isc_common.http.RPCResponse import RPCResponseConstant

from kaf_pas.ckk.models.item import Item
from kaf_pas.ckk.models.item_image_refs import Item_image_refs
from kaf_pas.ckk.models.item_line import Item_line
from kaf_pas.ckk.models.item_location import Item_location
from kaf_pas.ckk.models.item_refs import Item_refs
from kaf_pas.production.models.launch_item_line import Launch_item_line
from kaf_pas.production.models.launch_item_refs import Launch_item_refs
from kaf_pas.production.models.launch_operations_item import Launch_operations_item
from kaf_pas.production.models.operations_item import Operations_item
from kaf_pas.production.models.ready_2_launch_detail import Ready_2_launch_detail
from kaf_pas.sales.models.precent_items import Precent_items

logger = logging.getLogger(__name__)

class CombineItems(DSRequest):
    def __init__(self, request):
        DSRequest.__init__(self, request)
        data = self.get_data()

        recordTarget = data.get('recordTarget')
        if not isinstance(recordTarget, dict):
            raise Exception(f'recordTarget must be a dict')

        recordsSource = data.get('recordsSource')
        if not isinstance(recordsSource, list):
            raise Exception(f'recordsSource must be a list')

        # with transaction.atomic():
        for recordSource in recordsSource:
            if recordSource.get('id') != recordTarget.get('id'):
                for item_refs in Item_refs.objects.get_descendants(id=recordSource.get('id')):
                    item_refs.child_id = recordTarget.get('id')
                    try:
                        item_refs.save()
                    except Exception as ex:
                        logger.debug(ex)
                        item_refs.delete()

                for item_refs in Item_refs.objects.filter(parent_id=recordSource.get('id')):
                    item_refs.parent_id = recordTarget.get('id')
                    try:
                        item_refs.save()
                    except Exception as ex:
                        logger.debug(ex)
                        item_refs.delete()

                for item_image_refs in Item_image_refs.objects.filter(item_id=recordSource.get('id')):
                    item_image_refs.item_id = recordTarget.get('id')
                    try:
                        item_image_refs.save()
                    except Exception as ex:
                        logger.debug(ex)
                        item_image_refs.delete()

                for item_line in Item_line.objects.filter(child_id=recordSource.get('id')):
                    item_line.child_id = recordTarget.get('id')
                    try:
                        item_line.save()
                    except Exception as ex:
                        logger.debug(ex)
                        item_line.delete()

                for item_line in Item_line.objects.filter(parent_id=recordSource.get('id')):
                    item_line.parent_id = recordTarget.get('id')
                    try:
                        item_line.save()
                    except Exception as ex:
                        logger.debug(ex)
                        item_line.delete()

                for item_location in Item_location.objects.filter(item_id=recordSource.get('id')):
                    item_location.item_id = recordTarget.get('id')
                    try:
                        item_location.save()
                    except Exception as ex:
                        logger.debug(ex)
                        item_location.delete()

                for operations_item in Operations_item.objects.filter(item_id=recordSource.get('id')):
                    operations_item.item_id = recordTarget.get('id')
                    try:
                        operations_item.save()
                    except Exception as ex:
                        logger.debug(ex)
                        operations_item.delete()

                for launch_operations_item in Precent_items.objects.filter(item_id=recordSource.get('id')):
                    launch_operations_item.item_id = recordTarget.get('id')
                    try:
                        launch_operations_item.save()
                    except Exception as ex:
                        logger.debug(ex)
                        launch_operations_item.delete()

                for item_refs in Launch_item_refs.objects.filter(child_id=recordSource.get('id')):
                    item_refs.child_id = recordTarget.get('id')
                    try:
                        item_refs.save()
                    except Exception as ex:
                        logger.debug(ex)
                        item_refs.delete()

                for item_refs in Launch_item_refs.objects.filter(parent_id=recordSource.get('id')):
                    item_refs.parent_id = recordTarget.get('id')
                    try:
                        item_refs.save()
                    except Exception as ex:
                        logger.debug(ex)
                        item_refs.delete()

                for item_line in Launch_item_line.objects.filter(child_id=recordSource.get('id')):
                    item_line.child_id = recordTarget.get('id')
                    try:
                        item_line.save()
                    except Exception as ex:
                        logger.debug(ex)
                        item_line.delete()

                for item_line in Launch_item_line.objects.filter(parent_id=recordSource.get('id')):
                    item_line.parent_id = recordTarget.get('id')
                    try:
                        item_line.save()
                    except Exception as ex:
                        logger.debug(ex)
                        item_line.delete()

                for launch_operations_item in Launch_operations_item.objects.filter(item_id=recordSource.get('id')):
                    launch_operations_item.item_id = recordTarget.get('id')
                    try:
                        launch_operations_item.save()
                    except Exception as ex:
                        logger.debug(ex)
                        launch_operations_item.delete()

                for ready_2_launch_detail in Ready_2_launch_detail.objects.filter(item_id=recordSource.get('id')):
                    ready_2_launch_detail.item_id = recordTarget.get('id')
                    try:
                        ready_2_launch_detail.save()
                    except Exception as ex:
                        logger.debug(ex)
                        ready_2_launch_detail.delete()

                Item.objects.filter(id=recordSource.get('id')).delete()

        self.response = dict(status=RPCResponseConstant.statusSuccess)
