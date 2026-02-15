export default function DashboardLoading() {
  return (
    <div className="min-h-screen bg-[#F4F5F7] flex">
      {/* Sidebar Skeleton */}
      <aside className="w-64 bg-white border-r border-gray-200 flex flex-col shadow-sm">
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gray-200 rounded-lg animate-pulse"></div>
            <div className="w-20 h-6 bg-gray-200 rounded animate-pulse"></div>
          </div>
        </div>
        <nav className="flex-1 p-4 space-y-1">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="h-10 bg-gray-100 rounded-lg animate-pulse"></div>
          ))}
        </nav>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header Skeleton */}
        <header className="border-b border-gray-200 bg-white shadow-sm">
          <div className="px-8 py-5">
            <div className="w-48 h-8 bg-gray-200 rounded animate-pulse mb-2"></div>
            <div className="w-64 h-4 bg-gray-100 rounded animate-pulse"></div>
          </div>
        </header>

        {/* Dashboard Content Skeleton */}
        <main className="flex-1 p-8 overflow-auto">
          {/* Stats Cards Skeleton */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
                <div className="w-32 h-4 bg-gray-200 rounded animate-pulse mb-4"></div>
                <div className="w-24 h-10 bg-gray-200 rounded animate-pulse mb-2"></div>
                <div className="w-20 h-4 bg-gray-100 rounded animate-pulse"></div>
              </div>
            ))}
          </div>

          {/* Main Grid Skeleton */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
            {/* Risk Distribution Skeleton */}
            <div className="lg:col-span-2 bg-white rounded-lg border border-gray-200 p-8 shadow-sm">
              <div className="w-40 h-6 bg-gray-200 rounded animate-pulse mb-6"></div>
              <div className="h-64 bg-gray-100 rounded animate-pulse"></div>
            </div>

            {/* Top Customers Skeleton */}
            <div className="bg-white rounded-lg border border-gray-200 p-8 shadow-sm">
              <div className="w-40 h-6 bg-gray-200 rounded animate-pulse mb-6"></div>
              <div className="space-y-4">
                {[1, 2, 3, 4, 5].map((i) => (
                  <div key={i} className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-gray-200 rounded-full animate-pulse"></div>
                    <div className="flex-1">
                      <div className="w-32 h-4 bg-gray-200 rounded animate-pulse mb-2"></div>
                      <div className="w-24 h-3 bg-gray-100 rounded animate-pulse"></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Feature Cards Skeleton */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[1, 2, 3].map((i) => (
              <div key={i} className="bg-white rounded-lg border border-gray-200 p-8 shadow-sm">
                <div className="w-14 h-14 bg-gray-200 rounded-lg animate-pulse mb-6"></div>
                <div className="w-40 h-6 bg-gray-200 rounded animate-pulse mb-3"></div>
                <div className="w-full h-4 bg-gray-100 rounded animate-pulse mb-2"></div>
                <div className="w-3/4 h-4 bg-gray-100 rounded animate-pulse"></div>
              </div>
            ))}
          </div>
        </main>
      </div>
    </div>
  );
}
